from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import PARRequest
from django.contrib.auth.models import User
from .forms import SignUpForm, SearchForm, PARRequestForm, EmailTaskForm, ParStatusChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import PARRequest, ApprovalStage, UserProfile, EmailTask
from .email_utils import send_email
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test , login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from accounts.decorators import user_has_role
from accounts.models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import base64
from django.core.files.base import ContentFile
import json

@user_has_role
def main_page(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        # Add your search logic here, e.g., querying the model

    context = {
        'form': form,
        'results': results,
        'search_query': search_query,
    }

    return render(request, 'main_page.html', context)

@user_has_role
def search_results(request):
    if request.method=='POST':
        form = SearchForm(request.get)
        if form.is_valid():
           search_query = form.cleaned_data.get('search_query')
           category = form.cleaned_data.get('category')
           return redirect( 'search_results.html')
    else:
        form = SearchForm()



    context= {
        'form': form,


    }

    return render(request, 'search_results.html', context)


# def create_par(request):
#     if request.method == 'POST':
#         form = PARRequestForm(request.user)
#         print(form)
#         if form.is_valid():
#             form = form.cleaned_data.get('username')
#             par = form.save(commit=False)
#             par.user = request.user
#             par.save()
#             return redirect('par_list')
#     else:
#         form = PARRequestForm()

#         context = {
#             'form': form,
#         }
#         return render(request, 'create_par.html', context)


# def par_list(request):
#     pars = PARRequest.objects.filter(user=request.user.id)
#     context = {
#         'pars': pars,
#     }
#     return render(request, 'par_list.html', context)

@user_has_role
def par_list(request):
    if request.user.is_admin:
        # If the user is an admin, show all the PARs
        pars = PARRequest.objects.all()
    else:
        # If the user is not an admin, filter by the user's department
        pars = PARRequest.objects.filter(department=request.user.department)

    context = {
        'pars': pars,
        'par_status_choices': PARRequest.Par_status
    }
    return render(request, 'par_list_2.html', context)

@login_required(login_url='login')
def user_pars(request):
    all_pars = PARRequest.objects.all()
    total_par_count = PARRequest.objects.all().count()
    total_item = PARRequest.objects.aggregate(total_item_count=Sum('item'))
    total_item_count = total_item.get('total_item_count', 0)
    total_users = PARRequest.objects.aggregate(total_users_count=Sum('user'))
    total_users_count = total_users.get('total_users_count', 0)
    total_unite_price = PARRequest.objects.aggregate(total_unite_price_count=Sum('unite_price'))
    total_unite_price_count = total_unite_price.get('total_unite_price_count', 0)


    return render(request, 'user_pars/pars.html', {'all_pars': all_pars,
                                                   'total_par_count': total_par_count,
                                                   'total_item_count': total_item_count,
                                                   'total_users_count': total_users_count,
                                                   'total_unite_price_count': total_unite_price_count,
                                                   })


@api_view(['POST'])
def edit_par(request, par_id):
    par_id = request.data.get('par_id', None)
    par_action = request.data.get('action', None)
    user_par = PARRequest.objects.get(par_id=par_id)
    if request.method == 'POST':
        if par_action == 'approved':
            user_par.was_approved = True
            user_par.save()
        elif par_action == "pending":
            user_par.was_approved = False
            user_par.save()
        return Response({})
    return Response({})



# @user_has_role
# def create_par(request):
#     if request.method == 'POST':
#         form = PARRequestForm(request.POST)  # Initialize form with POST data
#         if form.is_valid():
#             par = form.save(commit=False)
#             par.user = request.user
#             par.created_at = datetime.now()  # Fill created_at when a new request is created
#             par.save()
#             return redirect('par_list')
#     else:
#         form = PARRequestForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'create_par_2.html', context)
@user_has_role
def create_par(request):
    if request.method == 'POST':
        print(request.FILES)
        form = PARRequestForm(request.POST, request.FILES)  # Initialize form with POST data
        if form.is_valid():
            par = form.save(commit=False)
            par.user = request.user
            print(par.attachment)
            par.save()
            return redirect('par_list')
        else:
            # If the form is not valid, print the errors to the console (for debugging)
            # and send them back to the template to inform the user.
            print(form.errors)  # Debug: Print errors to the console
            messages.error(request, form.errors)  # Display form errors in the template
    else:
        form = PARRequestForm()

    context = {
        'form': form,
    }
    return render(request, 'create_par_2.html', context)

#Edit Par Status
@user_has_role
def change_par_status(request, par_id):
    par = get_object_or_404(PARRequest, id=par_id)
    if request.method == "POST" and request.user.is_admin:
        form = ParStatusChangeForm(request.POST, instance=par)
        if form.is_valid():
            form.save()
            messages.success(request, 'PAR status updated successfully!')
        else:
            messages.error(request, 'Error updating PAR status.')
    return HttpResponseRedirect(reverse('par_list'))


@user_has_role
def create_email_task(request):
    if request.method == 'POST':
        form = EmailTaskForm(request.POST)
        if form.is_valid():
            email_task = EmailTask(
                recipient=form.cleaned_data['recipient'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                send_at=form.cleaned_data['send_at']
            )
            email_task.save()
            return redirect('task_list')  # Redirect to the list of email tasks
    else:
        form = EmailTaskForm()

    return render(request, 'email_task_form.html', {'form': form})

@user_has_role
def send_notification_email(request):
    subject = 'Due date is close!'
    message = 'This is a notification email.'
    recipient_list = ['recipient@example.com']
    send_email(subject, message, recipient_list)




def dash(request):
    return render(request, 'dash.html')

@user_has_role
def par_detail(request, par_id):
    par = get_object_or_404(PARRequest, id=par_id)
    return render(request, 'par_detail.html', {'par': par})

# @user_has_role
# def edit_pars(request, par_id):
#     par = get_object_or_404(PARRequest, id=par_id)

#     if request.method == 'POST':
#         form = PARRequestForm(request.POST, instance=par)
#         if form.is_valid():
#             form.save()
#             return redirect('par_detail', par_id=par.id)

#     else:
#         form = PARRequestForm(instance=par)

#     return render(request, 'edit_par.html', {'form': form, 'par': par})
@user_has_role
def edit_pars(request, par_id):
    par = get_object_or_404(PARRequest, id=par_id)
    if request.method == 'POST':
        # Make sure to include request.FILES for file handling
        form = PARRequestForm(request.POST, request.FILES, instance=par)
        if form.is_valid():
            form.save()
            return redirect('par_detail', par_id=par.id)
        else:
            # If the form is not valid, you might want to print form.errors to debug
            print(form.errors)
    else:
        form = PARRequestForm(instance=par)

    return render(request, 'edit_par.html', {'form': form, 'par': par})


@login_required
def sign_pdf(request, par_id):
    par = get_object_or_404(PARRequest, id=par_id)
    if request.user != par.user and not request.user.is_admin:
        return redirect('par_list')  # or wherever you want to redirect unauthorized users
    context = {'par': par}
    return render(request, 'sign_pdf.html', context)

@require_POST
@login_required
def save_signed_pdf(request, par_id):
    par = get_object_or_404(PARRequest, id=par_id)
    if request.user != par.user and not request.user.is_admin:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        signed_pdf_data = data.get('signed_pdf')
        if signed_pdf_data:
            # Remove the prefix from the base64 string
            format, imgstr = signed_pdf_data.split(';base64,')
            ext = format.split('/')[-1]
            
            # Decode the base64 string
            decoded_file = base64.b64decode(imgstr)
            
            # Save the file
            filename = f'signed_par_{par.id}.{ext}'
            par.signed_attachment.save(filename, ContentFile(decoded_file), save=True)
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No PDF data received'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
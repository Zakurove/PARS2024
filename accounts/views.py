from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from .forms import CustomAuthenticationForm
from .decorators import user_has_role



# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('/')  # Redirect to the user's profile page after registration
#     else:
#         form = CustomUserCreationForm()

#     return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('/')
        else:
            messages.error(request, 'There was an error during registration. Please check your inputs.')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('/')  # Or wherever you want to redirect after login
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


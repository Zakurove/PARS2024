from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PARRequest, EmailTask

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)
    category = forms.ChoiceField(choices=[('category', 'Category'), ('status', 'Status'), ('business unit (BU)', 'Business unit (BU)'), ('duration', 'Duration'), ('vendor name', 'Vendor name'), ('contract name', 'Contract name')], required=False)



class PARRequestForm(forms.ModelForm):
    class Meta:
        model = PARRequest
        fields = ['department', 'item', 'quantity', 'status', 'category', 'unite_price',  'chosen_date', 'attachment']
        exclude = ['created_at']
        widgets = {
            'chosen_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ParStatusChangeForm(forms.ModelForm):
    class Meta:
        model = PARRequest
        fields = ['status']

class EmailTaskForm(forms.ModelForm):
    class Meta:
        model = EmailTask
        fields = ['recipient', 'subject', 'message', 'send_at',]
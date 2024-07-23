from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'mobile_number', 'job_title', 'department', 'profile_picture']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser  # Use your custom user model
#         fields = ('email', 'first_name', 'last_name', 'profile_picture', 'other_field')  # Add additional fields as needed


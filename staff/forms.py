from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Staff

class StaffForm(UserCreationForm):
    class Meta:
        model = Staff
        fields = ['username', 'email', 'roles', 'password1', 'password2']
        
        
class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'
                                      }),
        error_messages={'required': 'Please enter your username.'},
    )
    password = forms.CharField(
        error_messages={'required': 'Please enter your password.'},
    )
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'password1', 'password2']

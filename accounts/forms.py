from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_("username"), max_length=50)
    password = forms.CharField(label=_("password"), max_length=50, widget=forms.PasswordInput)


class EmailLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'password1', 'password2']

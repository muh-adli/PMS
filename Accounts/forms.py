from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Username',}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Password',}
        )
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Username',}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Password',}
        )
    )
    password2 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Password Again',}
        )
    )
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Email',}
        ),
    )
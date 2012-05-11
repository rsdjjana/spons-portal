from django import forms
from portal.models import *
from django.utils import html

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

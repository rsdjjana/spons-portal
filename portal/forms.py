from django import forms
from portal.models import *
from django.utils import html

class LoginForm(forms.Form):
    username=forms.CharField(help_text='Your Shaastra 2013 username')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password')

class RegisterForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput,help_text='enter a password which you can remeber')#add password again
	email=forms.EmailField()
	phonenumber=forms.CharField()

class AddCategoryForm(forms.Form):
	name=forms.CharField()
	info=forms.CharField(widget=forms.Textarea)
	
STATUS_CHOICES=(
('Sold','Sold'),
('Available','Available'),
)

IMAGE_CHOICES=(
('Yes','Yes'),
('No','No'),
)

class AddEventForm(forms.Form):
	name=forms.CharField()
	info=forms.CharField(widget=forms.Textarea)
	status=forms.ChoiceField(choices=STATUS_CHOICES)

class AddImageForm(forms.Form):
	image=forms.ImageField(required=False)


from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
	user=models.ForeignKey(User)
	phonenumber=models.CharField(max_length=40)

class Category(models.Model):
	name=models.CharField(max_length=100)
	info=models.TextField(max_length=1500)
	def __unicode__(self):
		return self.name

STATUS_CHOICES=(
('Sold','Sold'),
('Available','Available'),
)	

class Event(models.Model):
	name=models.CharField(max_length=100)
	category=models.ForeignKey(Category)
	info=models.TextField(max_length=1500)
	status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='Available')
	def __unicode__(self):
		return self.name



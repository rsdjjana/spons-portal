from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
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

"""
	having separate class for image enables any number of images being made associated with each category and event
"""

class CategoryImage(models.Model):
	name=models.CharField(max_length=1000)
	image=models.ImageField(upload_to='/media/photos/',null=True,blank=True)
	category=models.ForeignKey(Category)
	def __unicode__(self):
		return self.name

class EventImage(models.Model):
	name=models.CharField(max_length=1000)
	image=models.ImageField(upload_to='/media/photos/',null=True,blank=True)
	event=models.ForeignKey(Event)
	def __unicode__(self):
		return self.name


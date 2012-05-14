# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from portal.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from portal.models import *
from django.contrib import auth


def log_in(request):
    #if request.user.is_authenticated():
    #return HttpResponseRedirect("/home")   
    if (request.method=='POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
			inputs = form.cleaned_data
			user = auth.authenticate(username=inputs['username'],password=inputs['password'])
			if user is not None and user.is_active==True:
				auth.login(request,user) 
				return HttpResponseRedirect("/")
			else:
				return HttpResponse("username or password incorrect ")
        
        else:
			return HttpResponse("Username or password invalid")    
	
    else:
		form=LoginForm()
    return render_to_response("login.html",locals(),context_instance=RequestContext(request))

def register(request):
	if request.method=='POST':
		form=RegisterForm(request.POST)
		if form.is_valid():
			inputs=form.cleaned_data
			user=User.objects.create_user(inputs['username'],inputs['email'],inputs['password'])
			user.save()
			userprofile=UserProfile(user=user,phonenumber=inputs['phonenumber'])
			userprofile.save()
			return HttpResponseRedirect('/login')
	else:
		form=RegisterForm()
	return render_to_response("register.html",locals(),context_instance=RequestContext(request))

    
def home(request):
	logged_in=False
	if request.user.is_authenticated():
		logged_in=True
	categories=Category.objects.all()
	return render_to_response("home.html",{'categories':categories,'logged_in':logged_in},context_instance=RequestContext(request))

def add_category(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			form=AddCategoryForm(request.POST)
			if form.is_valid():
				inputs=form.cleaned_data
				category=Category(name=inputs['name'],info=inputs['info'])
				category.save()
				return HttpResponseRedirect('/')
	

		else:
			form=AddCategoryForm()
		return render_to_response("add_category.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()

def edit_category(request,categoryid):
	if request.user.is_authenticated():
		if request.method=='POST':
			form=AddCategoryForm(request.POST)
			if form.is_valid():
				inputs=form.cleaned_data
				category=Category.objects.get(id=categoryid)
				category.name=inputs['name']
				category.info=inputs['info']
				category.save()
				return HttpResponseRedirect('/')
		else:
			category=Category.objects.get(id=categoryid)
			form=AddCategoryForm()
		return render_to_response("edit_category.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()

def delete_category(request,categoryid):
	if request.user.is_authenticated():
		category=Category.objects.get(id=categoryid)
		category.delete()
		return HttpResponseRedirect('/')
	else:
		raise Http404()

def view_events(request,offset):
	logged_in=False
	if request.user.is_authenticated():
		logged_in=True
	category=Category.objects.get(id=offset)
	events=Event.objects.filter(category=category)
	return render_to_response("view_events.html",locals(),context_instance=RequestContext(request))
	

def add_events(request,offset):
	logged_in=False
	if request.user.is_authenticated():	
		logged_in=True
		if request.method=='POST':
			category=Category.objects.get(id=offset)			
			form=AddEventForm(request.POST)
			if form.is_valid():
				inputs=form.cleaned_data
				event=Event(name=inputs['name'],info=inputs['info'],category=category,status=inputs['status'])
				event.save()
				return HttpResponseRedirect("/category/"+str(category.id))
		else:
			category=Category.objects.get(id=offset)
			form=AddEventForm()
		return render_to_response("add_event.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()

def edit_event(request,categoryid,eventid):
	if request.user.is_authenticated():
		if request.method=='POST':
			form=AddEventForm(request.POST)
			if form.is_valid():
				inputs=form.cleaned_data
				event=Event.objects.get(id=eventid)
				event.name=inputs['name']
				event.info=inputs['info']
				event.status=inputs['status']
				event.save()
			return HttpResponseRedirect("/category/"+str(categoryid))
		else:
			event=Event.objects.get(id=eventid)
			form=AddEventForm()
			if event.status=='Sold':
				present_status=True
			else:
				present_status=False
			return render_to_response("edit_event.html",locals(),context_instance=RequestContext(request))
			
	else:
		raise Http404()
   


def delete_event(request,categoryid,eventid):
	if request.user.is_authenticated():
		event=Event.objects.get(id=eventid)
		event.delete()
		return HttpResponseRedirect('/category/'+str(categoryid))
	else:
		raise Http404()

 
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login")    

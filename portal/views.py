# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from portal.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from portal.models import *
from django.contrib import auth
from django.core.files import File
from settings import *


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
"""
	The home page will show all the categories for the sponsor
	The cores will be able to add categories, (name, info, photo), edit and delete stuff related to category there
"""
    
def home(request):
	logged_in=False
	if request.user.is_authenticated():
		logged_in=True
	categories=Category.objects.all()
	return render_to_response("home.html",{'categories':categories,'logged_in':logged_in},context_instance=RequestContext(request))

"""
	To save the image file to the respective directory
	#what is the 'wb' there for?
"""
def save_file(file,path=''):
	filename = file._get_name()
	fd = open('%s%s' % (MEDIA_ROOT,str(filename)), 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()
"""
	function to add a category, (name, info)
"""

def add_category(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			form=AddCategoryForm(request.POST)
			if form.is_valid():
				inputs=form.cleaned_data
				category=Category(name=inputs['name'],info=inputs['info'])
				category.save()
				return HttpResponseRedirect('/add_category_image/'+str(category.id))
				

		else:
			form=AddCategoryForm()
		return render_to_response("add_category.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()
"""
	To add the respective categories image(required=False)
"""

def add_category_image(request,categoryid):
	if request.user.is_authenticated():
		if request.method=='POST':
			form=AddImageForm(request.POST,request.FILES)
			if form.is_valid() and form.is_multipart():
				if request.FILES:
					category=Category.objects.get(id=categoryid)
					inputs=form.cleaned_data
					category_image=CategoryImage(name=request.FILES['image']._get_name(),category=category)
					save_file(request.FILES['image'])
					category_image.save()
				return HttpResponseRedirect('/')
		else:
			category=Category.objects.get(id=categoryid)
			form=AddImageForm()
			return render_to_response("add_category_image.html",{'category':category,'form':form},context_instance=RequestContext(request))	
	else:
		raise Http404()

"""
	To edit category info(name,info)
	The previous data will be shown in the edit form during editing
"""

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
				return HttpResponseRedirect('/edit_category/image/'+str(categoryid))
		else:
			category=Category.objects.get(id=categoryid)
			form=AddCategoryForm(initial={'name':category.name,'info':category.info})
		return render_to_response("edit_category.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()
"""
	To edit(change/add if not added before) the category image
"""

def edit_category_image(request,categoryid):
	if request.user.is_authenticated():
		category=Category.objects.get(id=categoryid)
		if request.method=='POST':
			form=AddImageForm(request.POST,request.FILES)
			if form.is_valid():
				if request.FILES:
					category_image=CategoryImage.objects.filter(category=category)
					if category_image:
						category_image1=CategoryImage.objects.get(category=category)
						category_image1.category=category
						category_image1.name=request.FILES['image']._get_name()
						save_file(request.FILES['image'])
						category_image1.save()
					else:
						category_image=CategoryImage(name=request.FILES['image']._get_name(),category=category)
						save_file(request.FILES['image'])
						category_image.save()
				return HttpResponseRedirect('/')
		else:
			category_image=CategoryImage.objects.filter(category=category)
			if category_image:
				category_image1=CategoryImage.objects.get(category=category)
				form=AddImageForm(initial={'name':category_image1.name,'image':category_image1.image,'category':category_image1.category})
			else:
				form=AddImageForm()
			return render_to_response("edit_category_image.html",locals(),context_instance=RequestContext(request))
			
	else:
		raise Http404()
"""
	To delete the category model instance
"""
	

def delete_category(request,categoryid):
	if request.user.is_authenticated():
		category=Category.objects.get(id=categoryid)
		category_image=CategoryImage.objects.filter(category=category)
		category_image.delete()
		category.delete()
		return HttpResponseRedirect('/')
	else:
		raise Http404()
"""
	To veiw all the event under a particular category selected
	The cores will be able to add,edit,delete event information
"""

def view_events(request,categoryid):
	logged_in=False
	if request.user.is_authenticated():
		logged_in=True
	category=Category.objects.get(id=categoryid)
	events=Event.objects.filter(category=category)
	category_image=CategoryImage.objects.filter(category=category)
	return render_to_response("view_events.html",locals(),context_instance=RequestContext(request))

def view_event_image(request,categoryid,eventid):
	event=Event.objects.get(id=eventid)
	event_image=EventImage.objects.filter(event=event)
	return render_to_response("view_event_details.html",locals(),context_instance=RequestContext(request))

"""
	To add events , (name, info, image(required=False))
"""	

def add_events(request,categoryid):
	logged_in=False
	if request.user.is_authenticated():	
		logged_in=True
		if request.method=='POST':
			category=Category.objects.get(id=categoryid)			
			form=AddEventForm(request.POST)
			if form.is_valid():
				inputs=form.cleaned_data
				event=Event(name=inputs['name'],info=inputs['info'],category=category,status=inputs['status'])
				event.save()
				return HttpResponseRedirect("/add_event_image/"+str(category.id)+"/"+str(event.id))
		else:
			category=Category.objects.get(id=categoryid)
			form=AddEventForm()
		return render_to_response("add_event.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()

def add_event_image(request,categoryid,eventid):
	if request.user.is_authenticated():
		if request.method=='POST':
			form=AddImageForm(request.POST,request.FILES)
			if form.is_valid() and form.is_multipart():
				if request.FILES:
					event=Event.objects.get(id=eventid)
					inputs=form.cleaned_data
					event_image=EventImage(name=request.FILES['image']._get_name(),event=event)
					save_file(request.FILES['image'])
					event_image.save()
				return HttpResponseRedirect('/category/'+str(categoryid))
		else:
			event=Event.objects.get(id=eventid)
			form=AddImageForm()
			return render_to_response("add_event_image.html",locals(),context_instance=RequestContext(request))	
	else:
		raise Http404()
"""
	To edit event related information
"""

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
			return HttpResponseRedirect("/edit_event/image/"+str(categoryid)+"/"+str(eventid))
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

"""
	To edit( change/add ) event images
"""

def edit_event_image(request,categoryid,eventid):
	if request.user.is_authenticated():
		category=Category.objects.get(id=categoryid)
		event=Event.objects.get(id=eventid)
		if request.method=='POST':
			form=AddImageForm(request.POST,request.FILES)
			if form.is_valid():
				if request.FILES:
					event_image=EventImage.objects.filter(event=event)
					if event_image:
						event_image1=EventImage.objects.get(event=event)
						event_image1.event=event
						event_image1.name=request.FILES['image']._get_name()
						save_file(request.FILES['image'])
						event_image1.save()
					else:
						event_image=EventImage(name=request.FILES['image']._get_name(),event=event)
						save_file(request.FILES['image'])
						event_image.save()
				return HttpResponseRedirect('/category/'+str(categoryid))
		else:
			event_image=EventImage.objects.filter(event=event)
			if event_image:
				event_image1=EventImage.objects.get(event=event)
				form=AddImageForm(initial={'name':event_image1.name,'image':event_image1.image,'event':event_image1.event})
			else:
				form=AddImageForm()
			return render_to_response("edit_event_image.html",locals(),context_instance=RequestContext(request))
	else:
		raise Http404()
   
"""
	To delete event instance
"""

def delete_event(request,categoryid,eventid):
	if request.user.is_authenticated():
		event=Event.objects.get(id=eventid)
		event_image=EventImage.objects.filter(event=event)
		event_image.delete()
		event.delete()
		return HttpResponseRedirect('/category/'+str(categoryid))
	else:
		raise Http404()

 
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login")    

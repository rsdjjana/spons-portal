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
                return HttpResponse("Username not valid")    
    else:
        form = LoginForm()
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
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))
    
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login")    

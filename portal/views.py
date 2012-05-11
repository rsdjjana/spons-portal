# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
        
    if (request.method=='POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            user = authenticate(username=inputs['username'],password=inputs['password'])
            if user is not None:
                login(request,user)
                return HttpResponseRedirect("/home")
            else:
                return HttpResponse("Username not valid")    
    else:
        form = LoginForm()
    return render_to_response("login.html",locals(),context_instance=RequestContext(request))
    
def home(request):
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))
    
def logout(request):
    logout(request)
    return HttpResponseRedirect("/")    

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

# Create your views here.
def register(request):

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)
        messages.success(request,"Successfully registered.")
        return redirect("index")
    else:
        context = {
           "form" : form
        }
        return render(request,"register.html",context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password=password)
        if user is None:
            messages.error(request,"Username or password invalid!")
            return render(request,"login.html", context)
        else:
            messages.success(request, "Successfully authenticated.")
            login(request,user)
            #return redirect("index")
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,"login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Successfully logged out.")
    return redirect("index")
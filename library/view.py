from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render

from Books.utils import check_internet


def home(request):
    internet=check_internet()
    return render(request,'index.html',{'internet':internet})

# @login_required
def loginview(request):
    if request.method=='POST':
        loginuser=request.POST.get('username')
        loginpassword=request.POST.get('password')
        user=authenticate(username=loginuser,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,'SuccessFully Logged In!')
            return redirect('home')
        
        else:
            messages.error(request,'Invalid Crendentials , Please try again!')
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

# @login_required
def registerview(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        lname=request.POST.get('lname')
        fname=request.POST.get('fname')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request,'Password not Match')
            return redirect('home')
        


        myuser=User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"You Library Account Was Created!")

        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
    
@login_required
def logoutview(request):
    logout(request)
    messages.success(request,'Successfully Logged Out !')
    return redirect('home')
    






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from subprocess import check_output, run, PIPE
import sys 
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Log In & Log Out Views

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            login(request,user)
            return redirect('/stonefundingapp/report', pk=user.username)
        else:
            print("Login Failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Details")
    else:
        return render(request, 'index.html',{})

@login_required
def report(request):
    return render(request, 'report.html')

@login_required
def bot(request):
    out = run([sys.executable, 'C://Users//Maisum Abbas//stonefunding//stonefundingapp//bot.py'])
    return redirect('/stonefundingapp/report/')
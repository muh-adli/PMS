from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import *

# Create your views here.
def LandingPage(request):

    Title = "Palm Management System"
    html = "accounts/LandingPage.html"
    form = LoginForm()

    if request.method == 'POST':
        # print("masuk post")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print(password, username)
            user = authenticate(request, username=username, password=password)
            # print(user)
            if user is not None:
                login(request, user)
                messages.success(request, "Credentials Valid")
                return redirect('HomePage')
        else:
            # print("invalid")
            messages.error(request, "Invalid Credentials")
            # return render(request, "LoginPage.html")
    context = {
        'Title':Title,
        'form':form,
    }
    return render(request, html, context)

def LogoutUser(request):
    logout(request)
    messages.warning(request, "Logout")
    return redirect('LandingPage')

def Register(request):
    if request.method == 'POST':
        # print("masuk post")
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        Passwordagain = request.POST.get('Passwordagain')
        Email = request.POST.get('Email')
        # print(Password, Username)
        # print(user)
        if Username and Password and Email is not None:
            if Password == Passwordagain:
                user = User.objects.create_user(username=Username,
                                                email=Email,
                                                password=Password)
                user.save()
                messages.info(request, "Credentials Created")
                return redirect('LandingPage')
            else:
                messages.info(request, "Password didn't match")
                return redirect('LandingPage')
        else:
            # print("invalid")
            messages.error(request, "Invalid Data")
            return redirect('LandingPage')
    # print("tidak post")
    return redirect('LandingPage')
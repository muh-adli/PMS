from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import *

# Create your views here.
def LandingPage(request):

    Title = "Palm Management System"
    html = "accounts/LandingPage.html"
    formlogin = LoginForm()
    formregis = RegisterForm()

    if request.method == 'POST':
        # print("masuk post")
        if 'login' in request.POST:
            print("MASOK LOGIN")
            form = LoginForm(request.POST)
            if form.is_valid():
                print("FORM VALID")
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # print(password, username)
                user = authenticate(request, username=username, password=password)
                # print(user)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Credentials Valid")
                    print("BERHASIL LOGIN")
                    return redirect('HomePage')
                else:
                    print("USER GA NEMU")
                    messages.error(request, "Invalid Credentials")
            else:
                print("ERROR LOGIN")
                messages.error(request, "Error Login")
        if 'register' in request.POST:
            print("MASOK REGISTER")
            form = RegisterForm(request.POST)
            if form.is_valid():
                print("FORM REGIS VALID")
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    print("PASS SAMA")
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password1']
                    email = form.cleaned_data['email']
                    user = User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, "User Created")
                    return redirect('LandingPage')
                else:
                    messages.error(request, "Password didn't same")
            else:
                print("FORM REGIS ERROR")
                messages.error(request, "Error Register")
    context = {
        'Title':Title,
        'regis':formregis,
        'login':formlogin,
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
                messages.info(request, "User Created")
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
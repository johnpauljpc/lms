from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .emailBackend import EmailBackend
from django.contrib.auth.forms import PasswordResetForm
# Create your views here.

def registrationView(request):
    # user = User.objects.all()

    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        username = request.POST['username']
        print('**************===========================')
        print(request.POST)

        #check if username exists
        if User.objects.filter(username = username).exists():
            messages.warning(request, f"the username <b>{username}</b> already exists!")
            return redirect('register')
        #check if email already exists

        if User.objects.filter(email = email ).exists():
            messages.warning(request, f'the email: <b>{email}</b> has been taken already!')
            return redirect('register')
        
        if password1 != password2:
            messages.info(request, 'password does not match')
            return redirect('register')

        user = User.objects.create_user(username = username, email = email)
        user.set_password(password1)
        user.save()
        messages.success(request, f'welcome  <b>{user.username}! You can now login')
        return redirect('login')
      

    return render(request, 'accounts/register.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = EmailBackend.authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/login.html')

def logoutView(request):
    if (request.method == 'POST' or request.method == 'GET'):
        logout(request)
        messages.info(request, 'You have logged out')
        return redirect('home')
    messages.info(request, 'You have NOT logged out')
    return redirect('/')

def resetPassword(request):
    pass


def resetPasswordDone(request):
    pass

def resetPasswordConfirm(request):
    pass


def resetPasswordComplete(request):
    pass
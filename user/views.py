from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, UserCreationForm, LoginForm
from django.contrib.auth.models import User
from django_email_verification import send_email
from django.contrib import messages

def index(request):
    return render(request, 'index.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data['email']
            user_username = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']
            user = User.objects.create_user(username=user_username, email=user_email, password=user_password)
            user.is_active = False 
            send_email(user)
            messages.add_message(request, messages.SUCCESS, "El link para activar tu cuenta fue enviado.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

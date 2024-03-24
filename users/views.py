from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def userRegister(request):
    if request.method == "POST":
        form = Account(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
    else:
        form = Account()
    return render(request, 'register.html', {'form': form})

def userLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect('store')  # Adjust this to your actual redirect URL
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

def userLogout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('store')  # Adjust this to your actual redirect URL




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('store')  # Redirect to a success page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password.html', {'form': form})
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
# Create your views here.

def login_view(requsest):    
    title = "Login"
    form = UserLoginForm(requsest.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(requsest, user)
        return redirect("/")
        # print(requsest.user.is_authenticated())

    return render(requsest, "form.html", {"form":form, "title": title})

def register_view(requsest):
    title = "Register"
    form = UserRegisterForm(requsest.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(requsest, new_user)
        return redirect("/")
    context = {
        "form": form,
        "title": title,

    }
    return render(requsest, "form.html", context)

def logout_view(requsest):
    logout(requsest)
    return redirect("/")

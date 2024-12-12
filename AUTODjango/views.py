from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegistrationForm




def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "successfully registered..!!!")
            return redirect("register")
        else:
            return render(request, "register.html", {"form": form})
            
    form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data["username"]
            password = data["password"]
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")
        else:
            context = {"form": form}
            return render(request, "login.html", context)
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("home")
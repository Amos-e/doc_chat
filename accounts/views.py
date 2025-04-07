from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

def signup_view(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:prompt")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }

    return render(request, "accounts/signup.html", context)


def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main:prompt")
    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(request, "accounts/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("main:index")
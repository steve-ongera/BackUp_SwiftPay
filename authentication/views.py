# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from .forms import LoginForm, SignUpForm
from django.contrib import messages


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid username or password!'
        else:
            msg = 'An error occurred!.'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            messages.success(request, 'User created successfully. ')
            return redirect('authentication:login')
        else:
            # Show the form errors for debugging
            print(form.errors)  # This will output errors in the console or logs
            messages.error(request, 'Form is not valid')
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})



def custom_logout(request):
    # Log the user out
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('/')  # Redirect to login page or any other page


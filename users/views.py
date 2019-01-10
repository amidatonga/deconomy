from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistration
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Username {username} was successfully created! Please enter your login and password.')
            return redirect('auth')



    else:
        form = UserRegistration()

    return render(request, 'users/registration.html', {'form': form, 'title': 'User registration'})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

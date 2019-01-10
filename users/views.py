from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistration, ProfileUpdateForm, UserUpdateForm
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
def update_profile(request):
    if request.method == "POST":
        update_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        update_user = UserUpdateForm(request.POST, instance=request.user)

        if update_profile.is_valid() and update_user.is_valid():
            update_user.save()
            update_profile.save()
            messages.success(request, f'Your account successfully updated!')
            return redirect('profile')
    else:
        update_profile = ProfileUpdateForm(instance=request.user.profile)
        update_user = UserUpdateForm(instance=request.user)

    data  = {
        'update_profile': update_profile,
        'update_user': update_user
    }
    return render(request, 'users/update_profile.html', data)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

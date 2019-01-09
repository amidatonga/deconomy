from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistration

def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Username {username} was successfully created!')
            return redirect('news_list')



    else:
        form = UserRegistration()

    return render(request, 'users/registration.html', {'form': form, 'title': 'User registration'})

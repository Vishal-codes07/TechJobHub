from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomCreationForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('job_list')

    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('job_list')
    else:
        form = CustomCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

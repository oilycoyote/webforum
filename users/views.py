from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib import messages


# Register User
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')


    else:
        form = SignUpForm()
    
    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

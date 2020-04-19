from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages


# Register User
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Account created for {first_name}!')
            return redirect('login')


    else:
        form = SignUpForm()
    
    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm( request.POST,instance = request.user)
        p_form = ProfileUpdateForm( request.POST,request.FILES, instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            first_name = u_form.cleaned_data.get('first_name')
            messages.success(request, f'Account updated for {first_name}')
            return redirect('profile')
        

    else:    
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):  # # User registration view
    # if we get the post request then we will try to validate that form data
    if request.method == 'POST': 
        form =  UserRegisterForm(request.POST)
        if form.is_valid(): # validating
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created!')# one time alert
            return redirect('login') # redirecting to login oage
    else:
        form =  UserRegisterForm()
    return render(request, 'users/register.html', {'form': form}) 
    # access the form within the template

@login_required # This will not allow to view profile without login
def profile(request):  # User's profile view
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile. Please check the form.')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)
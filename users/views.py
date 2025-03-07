from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import RegisterUserForm, UserForm

# Create your views here.


def register_view(request):
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form)
            return redirect('blog:home')
        messages.error('Something went wrong')
    return render(request, 'users/register_login.html', {'form':form})


def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('blog:home')
        else:
            messages.error(request, 'Password does not exist')
    context = {'page':page}
    return render(request, 'users/register_login.html', context)


def logout_view(request):
    logout(request)
    return redirect('blog:home')

@login_required
def user_profile_view(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def update_profile_view(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    return render(request, 'users/update-user.html', {'form':form})
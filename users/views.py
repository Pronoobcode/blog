from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from blog.models import BlogPost
from .forms import RegisterUserForm, UserForm

# Create your views here.


def register_view(request):
    page = 'register'
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('blog:home')
        messages.error(request, 'Something went wrong')
    return render(request, 'users/login_register.html', {'form': form, 'page': page})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('users:login')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('blog:home')
        else:
            messages.error(request, 'Password is incorrect')
    return render(request, 'users/login_register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')


@login_required(login_url='users:login')
def user_profile_view(request, pk):
    user = User.objects.get(id=pk)
    posts = BlogPost.objects.filter(created_by=user)
    context = {'user':user, 'posts':posts}
    return render(request, 'users/profile.html', context)


@login_required(login_url='users:login')
def update_profile_view(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    return render(request, 'users/update_user.html', {'form':form})

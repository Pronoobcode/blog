from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import BlogCategory, BlogPost, Message   

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = BlogPost.objects.filter(
        Q(category__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(created_by__username=q)
    )

    posts = BlogPost.objects.all()
    category = BlogCategory.objects.all()[0:5]
    blog_messages = Message.objects.filter(Q(BlogPost__category__name__icontains=q))
    paginator = Paginator(posts, 6)
    page_number = request.Get.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts':posts, 'page_obj':page_obj, 'category':category}
    return render(request, 'blog/home.html', context)



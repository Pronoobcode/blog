from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from .models import BlogCategory, BlogPost, Message 


# Create your views here.


def home_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blog_posts = BlogPost.objects.filter(
        Q(category__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(created_by__username=q)
    )

    blog_posts = BlogPost.objects.all()
    category = BlogCategory.objects.all()[0:5]
    post_messages = Message.objects.filter(Q(BlogPost__category__name__icontains=q))
    paginator = Paginator(blog_posts, 6)
    page_number = request.Get.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'blog_posts':blog_posts, 'page_obj':page_obj, 'category':category, 'post_messages':post_messages}
    return render(request, 'blog/home.html', context)


def post_view(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    post_messages = blog_post.message_set.all()
    participants = blog_post.participants.all()

    if request.Method == 'POST':
        message = Message.objects.create(
            user=request.user,
            blog_post=post,
            body=request.GET.get('body')
        )
        blog_post.participants.add(request.user)
        return redirect('blog_post', pk=blog_post.id)
    context = {'blog_post':blog_post, 'post_messages':post_messages, 'participants':participants}
    return render(request, 'blog/post.html', context)


@login_required(login_url='login')
def create_post_view(request):
    form = BlogPostForm()
    category = BlogCategory.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = BlogCategory.objects.get_or_create(name=category_name)

        BlogPost.objects.create(
            created_by=request.user,
            category=category,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            video=request.FILES.get('video')
        )
        return redirect('home')
    
    context = {'forms':form, 'category':category}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='login')
def update_post_view(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    form = BlogPostForm(instance=blog_post)
    categorys = BlogCategory.objects.all()
    if request.user != blog_post.created_by:
        messages.error(request, "You can't do that")
    
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = BlogCategory.objects.get_or_create(name=category_name)
        blog_post.title = request.Post.get('name')
        blog_post.category = category
        blog_post.description = request.POST.get('description')
        blog_post.save()
        return redirect('home')
    context = {'form':form, 'categorys':categorys, 'blog_post':blog_post}
    return render(request, 'blog/blog_form.html', context)


def delete_post_view(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    
    if request.user != blog_post.created_by:
        messages.error(request, "You can't do that")
    
    if request.method == 'POST':
        blog_post.delete()
        return redirect('home')
    return render(request, 'blog/delete.html', {'blog_post':blog_post})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.error(request, "You can't do that")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
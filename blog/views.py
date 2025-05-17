from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm, MessageForm
from .models import BlogPost, Message 


def home_view(request):
    q = request.GET.get('q', '')

    blog_posts = BlogPost.objects.filter(
        Q(category__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(created_by__username=q)
    )

    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blog_posts': blog_posts,
        'page_obj': page_obj,
    }
    return render(request, 'blog/home.html', context)


def post_view(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    post_messages = blog_post.message_set.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        body = request.POST.get('body')
        if body:
            Message.objects.create(
                user=request.user,
                blog_post=blog_post,
                body=body
            )
            blog_post.participants.add(request.user)
            messages.success(request, 'Your comment has been posted.')
            return redirect('blog:post', pk=blog_post.id)
        messages.error(request, 'Comment cannot be empty.')
    elif request.method == 'POST' and not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to comment.')
        return redirect('users:login')

    context = {
        'blog_post': blog_post,
        'post_messages': post_messages,
        'participants': blog_post.participants.all()
    }
    return render(request, 'blog/post.html', context)



@login_required(login_url='users:login')
def create_post_view(request):
    form = BlogPostForm()

    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')

        if not category or not title:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'blog/post_form.html', {'form': form})

        capitalized_title = ' '.join(word.capitalize() for word in title.split())

        media_file = request.FILES.get('image')

        blog_post = BlogPost.objects.create(
            created_by=request.user,
            category=category.capitalize(),
            title=capitalized_title,
            description=request.POST.get('description'),
            image=media_file
        )
        messages.success(request, 'Your post has been created successfully!')
        return redirect('blog:post', pk=blog_post.id)

    return render(request, 'blog/post_form.html', {'form': form})



@login_required(login_url='users:login')
def update_post_view(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    if request.user != blog_post.created_by:
        messages.error(request, "You can't do that.")
        return redirect('blog:home')

    form = BlogPostForm(instance=blog_post)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            blog_post = form.save(commit=False)
            
            # Capitalize title and category
            blog_post.title = ' '.join(word.capitalize() for word in blog_post.title.split())
            blog_post.category = blog_post.category.capitalize()
            blog_post.save()
            
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('blog:post', pk=blog_post.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm(instance=blog_post)

    context = {'form': form, 'blog_post': blog_post}
    return render(request, 'blog/post_form.html', context)



@login_required(login_url='users:login')
def delete_post_view(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)

    if request.user != blog_post.created_by:
        messages.error(request, "You can't do that")
        return redirect('blog:home')

    if request.method == 'POST':
        blog_post.delete()
        messages.success(request, 'Your post has been deleted.')
        return redirect('blog:home')

    return render(request, 'blog/delete.html', {'blog_post': blog_post})


@login_required(login_url='users:login')
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)
    post_id = message.blog_post.id 

    if request.user != message.user:
        messages.error(request, "You are not authorized to delete this message.")
        return redirect('blog:post', pk=post_id)

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Your comment has been deleted.')
        return redirect('blog:post', pk=post_id)

    context = {'obj': message}
    return render(request, 'blog/delete.html', context)


@login_required(login_url='users:login')
def update_message_view(request, pk):
    message = get_object_or_404(Message, pk=pk)
    post_id = message.blog_post.id

    if request.user != message.user:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('blog:post', pk=post_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            if form.cleaned_data['body'].strip():  
                form.save()
                messages.success(request, "Your comment has been updated.")
                return redirect('blog:post', pk=post_id)
            else:
                messages.error(request, "Comment cannot be empty.")
        else:
            messages.error(request, "There was an error updating your comment.")
    else:
        form = MessageForm(instance=message)

    context = {
        'form': form,
        'message': message,
    }
    return render(request, 'blog/update_message.html', context)


@login_required(login_url='users:login')
def category_view(request, category=None):
    user_messages = Message.objects.filter(user=request.user)
    user_posts = BlogPost.objects.filter(created_by=request.user)
    my_categories = list(BlogPost.objects.values_list('category', flat=True).distinct())
    categories = list(dict.fromkeys(my_categories))

    post_counts = {cat: BlogPost.objects.filter(category__iexact=cat).count() for cat in categories}

    if category:
        selected_posts = BlogPost.objects.filter(category__iexact=category)
    else:
        selected_posts = BlogPost.objects.none()  

    context = {
        'user_messages': user_messages,
        'user_posts': user_posts,
        'categories': categories,
        'selected_posts': selected_posts,
        'post_counts': post_counts,  
    }
    return render(request, 'blog/category.html', context)

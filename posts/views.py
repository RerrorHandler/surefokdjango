from datetime import timezone
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Favorite
from sells.models import sells
from .forms import PostDeleteForm, PostForm
from django.contrib import messages


def post_list(request):
    user = request.user
    posts = Post.objects.filter().order_by('-created_at')
    favorites = []
    if user.is_authenticated:
        favorites = Favorite.objects.filter(user_id=user.id, post__in=posts)
    posts_count = Post.objects.filter().count()
    favorite_count = Favorite.objects.filter(user_id=user.id).count()
    favorite_posts = favorites.values_list('post', flat=True) if favorites else []
    return render(request, 'posts/post_list.html', {'posts': posts, 'favorite_posts': favorite_posts, 'posts_count': posts_count, 'favorite_count': favorite_count })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            messages.success(request, 'Ваше объявление было успешно опубликовано!')
            post.save()
            return redirect('/posts/')
    else:
        form = PostForm()
    return render(request, 'posts/post_add.html', {'form': form})

def page(request):
    return render(request, 'posts/start-page.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, post=post).exists()
    return render(request, 'posts/post_detail.html', {'post': post, 'is_favorite': is_favorite})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostDeleteForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            post.delete()
            return redirect('posts:post_list')
    
    return render(request, 'posts/post_delete.html', {'post': post})
@login_required
def favorite_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
    messages.success(request, 'Ваше объявление было успешно добавлено в избранное!')
    return redirect('posts:post_list')
@login_required
def remove_favorite_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Favorite.objects.filter(user=request.user, post=post).delete()
    messages.success(request, 'Ваше объявление было успешно удалено из избранного!')
    return redirect('posts:post_list')
@login_required
def favorite_list(request):
    user = request.user
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    posts_count = Post.objects.filter().count()
    favorite_count = Favorite.objects.filter(user=user).count()
    return render(request, 'posts/favorite_list.html', {'favorites': favorites, 'posts_count': posts_count, 'favorite_count': favorite_count})


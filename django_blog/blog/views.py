from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    posts = Post.objects.order_by('-published_date')[:20]
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

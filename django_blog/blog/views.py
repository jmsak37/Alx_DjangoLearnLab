from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    posts = Post.objects.order_by('-published_date')[:20]
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm

def register(request):
    """
    Handle user registration. On successful registration the user is logged in and redirected.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally set additional defaults, e.g. user.email = form.cleaned_data['email']
            login(request, user)  # log in immediately after registration
            return redirect('home')  # change to your prefered landing page e.g. 'list_books'
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    """
    Allow the logged-in user to view and edit their profile (email here).
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

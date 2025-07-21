from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test  # ← import here
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from .models import Book, Library

# Role‑check helpers
def is_admin(user):
    return getattr(user, 'userprofile', None) and user.userprofile.role == 'Admin'

def is_librarian(user):
    return getattr(user, 'userprofile', None) and user.userprofile.role == 'Librarian'

def is_member(user):
    return getattr(user, 'userprofile', None) and user.userprofile.role == 'Member'

# Role‑protected views
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Basic Book/Library views
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # ← UserCreationForm() call
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

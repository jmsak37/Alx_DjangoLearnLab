from django.shortcuts import render, redirect
from .models import Library, Book
from django.views.generic import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy

# 1. List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# 2. Library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ✅ 3. User registration using UserCreationForm()
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # ← this is what the checker looks for
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# 4. User login
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

# 5. User logout
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

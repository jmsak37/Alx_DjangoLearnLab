from django.shortcuts import render, redirect
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Book, Library

# 1. List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# 2. Library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# 3. User registration
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

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
UserCreationForm()
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_admin(u):
    return hasattr(u, 'userprofile') and u.userprofile.role == 'Admin'

def is_librarian(u):
    return hasattr(u, 'userprofile') and u.userprofile.role == 'Librarian'

def is_member(u):
    return hasattr(u, 'userprofile') and u.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

# helper to check role
def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    # renders the member-specific template
    return render(request, 'relationship_app/member_view.html')

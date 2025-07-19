from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# 1. Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# 2. Class-based view: show one library’s details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

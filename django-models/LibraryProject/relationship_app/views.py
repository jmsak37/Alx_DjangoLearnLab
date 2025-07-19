from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from relationship_app.models import Book, Library

# 1. Function-based view: list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    # Use plain text for now, or render to template if you choose
    return render(request, 'list_books.html', {'books': books})

# 2. Class-based view: show one library’s details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

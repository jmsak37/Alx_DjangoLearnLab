from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


"""
api.views
Generic views for the Book model using Django REST Framework.
Provides:
 - BookListView      -> list all books (GET)
 - BookDetailView    -> retrieve single book (GET)
 - BookCreateView    -> create a book (POST)
 - BookUpdateView    -> update a book (PUT/PATCH)
 - BookDeleteView    -> delete a book (DELETE)

Read-only access is allowed to anyone. Create/Update/Delete require authentication.
"""

from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# -----------------------
# Book Views (CRUD)
# -----------------------

class BookListView(generics.ListAPIView):
    """
    GET /api/books/  -> List all books.
    Read-only for unauthenticated users.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view list


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/ -> Retrieve a single book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/ -> Create a new book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optional customization: validate/save hooks
    def perform_create(self, serializer):
        # If you needed to attach the request.user or do custom logic, do it here.
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/ -> Update a book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/ -> Delete a book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------
# Author Views (for completeness)
# -----------------------

class AuthorListView(generics.ListCreateAPIView):
    """
    GET /api/authors/ -> list authors
    POST /api/authors/ -> create author (authenticated)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    GET /api/authors/<pk>/ -> retrieve author + nested books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# List + filter + search + ordering
class BookListView(generics.ListCreateAPIView):
    """
    GET: lists books (supports ?search=, ?ordering=, ?<field>=value)
    POST: create book (requires appropriate permissions if you add them)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # enable filter backends (also set in settings.py)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # fields allowed for exact filtering via ?title=... or ?publication_year=...
    filterset_fields = ['title', 'publication_year', 'author']  # author id or exact

    # search: user can do ?search=term that matches these fields (text search)
    search_fields = ['title', 'author__name']

    # ordering: ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year']

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/PATCH/DELETE a single book by pk.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class BookList(generics.ListAPIView):
    """
    GET /api/books/ → returns JSON list of all books
    """
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, & destroy for Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

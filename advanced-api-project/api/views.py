from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

from django.urls import path
from .views import BookListCreateAPIView, AuthorListAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='api-books'),
    path('authors/', AuthorListAPIView.as_view(), name='api-authors'),
]

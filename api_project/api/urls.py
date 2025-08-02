from django.urls import path
from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
# 2) router for full CRUD:
router = DefaultRouter()

# registers under /api_app/books_all/ and /api_app/books_all/{pk}/
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns += [
    path('', include(router.urls)),
]
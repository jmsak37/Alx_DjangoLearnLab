from django.urls import path
from relationship_app.views import list_books, LibraryDetailView

urlpatterns = [
    # Function view: /books/
    path('books/', list_books, name='list_books'),

    # Class view: /libraries/<int:pk>/
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

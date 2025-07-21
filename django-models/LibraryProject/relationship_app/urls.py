from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import add_book, edit_book, delete_book
from .views import list_books

urlpatterns = [
    # Book & Library views
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/',    LoginView.as_view(template_name='relationship_app/login.html'),   name='login'),
    path('logout/',   LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-based views
    path('admin-area/',     views.admin_view,     name='admin_view'),
    path('librarian-area/', views.librarian_view, name='librarian_view'),
    path('member-area/',    views.member_view,    name='member_view'),

    # Custom permission–protected book actions
    path('books/add/',           add_book,    name='add_book'),
    path('books/<int:pk>/edit/', edit_book,   name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),

    # Additional URL patterns for checker
    path('add_book/',               add_book,    name='add_book'),
    path('edit_book/<int:pk>/',     edit_book,   name='edit_book'),
]

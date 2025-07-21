from django.urls import path
from .views import admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Book & Library views
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/',    LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/',   LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

urlpatterns += [
    path('admin-area/', admin_view, name='admin_view'),
    path('librarian-area/', librarian_view, name='librarian_view'),
    path('member-area/', member_view, name='member_view'),
]

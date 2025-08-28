# accounts/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView
from . import views

app_name = 'accounts'


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('following/', views.FollowingListView.as_view(), name='following_list'),
    path('followers/', views.FollowersListView.as_view(), name='followers_list'),
]

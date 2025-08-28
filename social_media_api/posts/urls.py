# posts/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet
from .views import FeedListView
from .views import LikePostAPIView, UnlikePostAPIView, FeedListView, PostViewSet
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', UnlikePostAPIView.as_view(), name='post-unlike'),
    path('feed/', FeedListView.as_view(), name='feed'),
]

# posts/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update, destroy for Posts.
    - Read: anyone (IsAuthenticatedOrReadOnly default)
    - Create/Update/Delete: authenticated and only owners for update/delete
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'created_at']  # example filters
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments. Only authors can edit/delete their comments.
    """
    queryset = Comment.objects.all().select_related('post', 'author')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author__username']
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        # If client posted a post id in data: use it; otherwise error will come from serializer
        serializer.save(author=self.request.user)

class FeedListView(generics.ListAPIView):
    """
    Feed: posts authored by users the current authenticated user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # or use your standard pagination class if you want paged feed

    def get_queryset(self):
        user = self.request.user
        # If unauthenticated the permission class will prevent access.
        following = user.following.all()
        return Post.objects.filter(author__in=following).order_by('-created_at')

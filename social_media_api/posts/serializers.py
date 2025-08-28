# posts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .models import Post, Like

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'likes_count', 'liked_by_user']
        read_only_fields = ['likes_count', 'liked_by_user']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)  # nested read-only comments

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at', 'comments']

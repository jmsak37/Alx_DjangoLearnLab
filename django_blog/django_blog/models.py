from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings
from django.db import models
from django.utils import timezone

User = get_user_model()

class Post(models.Model):
    """
    Blog Post model for django_blog.
    Fields:
    - title: short title
    - content: post body
    - published_date: automatically set on creation
    - author: FK to the User model (allow many posts per author)
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

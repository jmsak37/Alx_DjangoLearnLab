from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.conf import settings
from django.utils import timezone

from django.urls import reverse
User = get_user_model()

class Post(models.Model):
    """
    Blog Post model for django_blog.
    Fields:
    - title: short title
    - content: main body
    - published_date: automatically set on creation
    author: FK to the user that created the post (uses AUTH_USER_MODEL)
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})


# Comment model: attached to a Post and a User. Stores timestamps for created/updated.
class Comment(models.Model):
    # link to the Post model (assumes Post is defined in this module)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    # link to the configured user model (works with default or custom AUTH_USER_MODEL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

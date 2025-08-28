# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Generic notification model:
    - recipient: user who receives the notification
    - actor: user who performed the action (liker, commenter, follower)
    - verb: 'liked', 'commented', 'followed' etc
    - target/content_object: generic link to the object (post/comment/user)
    - read: whether recipient has seen it
    - timestamp
    """
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actor_notifications', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    # generic relation to any target
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification(to={self.recipient}, actor={self.actor}, verb={self.verb})"

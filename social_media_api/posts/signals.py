# posts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    liker = instance.user
    if post.author != liker:
        Notification.objects.create(
            recipient=post.author,
            actor=liker,
            verb='liked your post',
            target_ct=ContentType.objects.get_for_model(post),
            target_id=post.pk
        )

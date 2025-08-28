# notifications/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'actor_username', 'verb', 'target_repr', 'unread', 'timestamp']

    def get_target_repr(self, obj):
        # Friendly representation of the target (post title, comment text, or username)
        target = obj.target
        if target is None:
            return None
        # try common attributes
        for attr in ('title', 'content', 'username', 'get_full_name'):
            if hasattr(target, attr):
                value = getattr(target, attr)
                return value() if callable(value) else str(value)
        return str(target)

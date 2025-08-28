from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Extends AbstractUser with additional fields:
    - bio: short text about the user
    - profile_picture: optional image uploaded to MEDIA_ROOT/profiles/
    - followers: M2M to self, non-symmetrical (someone can follow you without you following back)
    """
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        # prefer username, fallback to email if used
        return self.username or str(self.email)

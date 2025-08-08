from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Author(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self): return self.name

class Book(models.Model):
    title = models.CharField(max_length=300)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def clean(self):
        if self.publication_year and self.publication_year > timezone.now().year:
            raise ValidationError({'publication_year': 'Publication year cannot be in the future.'})

    def __str__(self): return f"{self.title} ({self.publication_year})"

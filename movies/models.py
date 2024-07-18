from django.db import models
from django.contrib.auth.models import User
import uuid

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class Collection(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

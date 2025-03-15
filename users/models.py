from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=40, null=True)
    username = models.CharField(max_length=40, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="images/profile.webp")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []






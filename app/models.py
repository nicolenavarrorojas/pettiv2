from django.db import models
from django.contrib.auth.models import AbstractUser
from app.managers import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    is_administrator = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
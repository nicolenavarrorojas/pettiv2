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


class Service(models.Model):
    GROOMING = 'grooming'
    WALKING = 'walking'
    SITTING = 'sitting'
    SERVICE_TYPE_CHOICES = (
        (GROOMING, 'estética'),
        (WALKING, 'paseo'),
        (SITTING, 'cuidado'),
    )
    service_type = models.CharField(
        choices=SERVICE_TYPE_CHOICES,
        default=GROOMING,
        max_length=30
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='services'
    )
    image = models.ImageField(upload_to='service_images', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(default=1)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Reservation for {self.service.title} on {self.date} at {self.time} by {self.client.email}'

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar_choices = [
        ('avatar1', 'Avatar 1'),
        ('avatar2', 'Avatar 2'),
        ('avatar3', 'Avatar 3'),
    ]
    profile_avatar = models.CharField(max_length=20, choices=avatar_choices, default='avatar1')

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
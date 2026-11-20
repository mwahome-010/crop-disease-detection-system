from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        FARMER = 'FARMER', 'Farmer'
        ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.FARMER
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
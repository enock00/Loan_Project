from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from .managers import CustomUserManager
from django.conf import settings

class CustomUser(AbstractUser):
    username = None  # remove username
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d{9,15}$')]
    )
    id_no = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "full_name", "id_no"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.email})"


from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ("USER", "User"),
        ("ADMIN", "Admin"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES, default= "User")
    phone_number = models.CharField(max_length=11, blank=False, null=False)
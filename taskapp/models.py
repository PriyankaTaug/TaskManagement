from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomeUser(AbstractUser):
    ROLE_CHOICES = (
        ("superadmin","SuperAdmin"),
        ("admin","Admin"),
        ("user","User")
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="user")

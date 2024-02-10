from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    cv = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)

    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'first_name', 'last_name', 'email', 'password']

    def __str__(self):
        return self.username

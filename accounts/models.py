from django.contrib.auth.models import AbstractUser,User
from django.db import models
import random
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username', 'email']  # required by AbstractUser

    def __str__(self):
        return self.mobile

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"{random.randint(100000, 999999)}"  # 6-digit OTP
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


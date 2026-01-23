from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return self.mobile


class OTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    mobile = models.CharField(
    max_length=15,
    null=True,
    blank=True
)

    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    city = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

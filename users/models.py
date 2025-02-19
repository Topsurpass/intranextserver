from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('mentor', 'Mentor'), ('admin', 'Admin')],
        default='user'
    )
    password = models.CharField(max_length=128)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class UserProfile(models.Model):
    """User profile model for storing additional details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")    
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    profile_picture = models.URLField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

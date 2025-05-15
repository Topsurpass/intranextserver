from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import User, UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user_id=instance)

@receiver(post_delete, sender=get_user_model())
def delete_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete()
    except UserProfile.DoesNotExist:
        pass
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, UserPreferences


@receiver(post_save, sender=User)
def create_user_profile_and_preferences(sender, instance, created, **kwargs):
    """Автоматично створює профіль та переваги для нового користувача"""
    if created:
        UserProfile.objects.create(user=instance)
        UserPreferences.objects.create(user=instance) 
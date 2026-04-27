from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile, Restaurant

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        restaurant = Restaurant.objects.first()
        if restaurant:
            Profile.objects.create(user=instance, restaurant=restaurant)
            
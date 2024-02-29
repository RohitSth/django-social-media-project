# Adding django signal
from django.db.models.signals import post_save
from django.contrib.auth.models import User # sender
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender = User) 
# Signal to create a profile when a new user is created
def create_profile(sender, instance, created, **kwargs): 
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
# Signal to save the profile when the user is saved
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user = instance)       
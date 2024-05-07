from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Profile

@receiver(post_save, sender=User)
def create_profile_signal(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        
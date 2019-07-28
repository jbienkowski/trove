from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime

from .models import RijpModelBase, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Catch pre_save signal for all objects, but update its modified timestamp only
# if it is based on RijpModelBase
@receiver(pre_save)
def update_rijp_project(sender, instance, **kwargs):
    if issubclass(type(instance), RijpModelBase):
        instance.modified = datetime.now()

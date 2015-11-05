from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(Model):
    user = models.OneToOneField(User)
    email = models.EmailField(blank=True)


@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    instance = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        Profile.objects.create(user=instance)
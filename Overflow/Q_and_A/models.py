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


class Question(Model):
    asker = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    question = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)

class Answer(Model):
    question_answered = models.ForeignKey(Question)
    answerer = models.ForeignKey(User)
    answer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Tag(Model):
    title = models.CharField(max_length=25)
    description = models.TextField(blank=True)

class Vote(Model):
    type = models.CharField(max_length=6, choices=[('up', 'Up'), ('down', 'Down')])
    voter = models.ForeignKey(User)
    answer_voted = models.ForeignKey(Answer)
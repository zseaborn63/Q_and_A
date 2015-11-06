from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(Model):
    user = models.OneToOneField(User)
    email = models.EmailField(blank=True)

    @property
    def question_count(self):
        return self.user.question_set.all().count()

    @property
    def score(self):
        answer_scores = [self.question_count * 5]
        answers = self.user.answer_set.all()
        for answer in answers:
            answer_scores.append(answer.user_score)
        downvotes = Vote.objects.filter(voter=self.user, type='down')
        for downvote in downvotes:
            answer_scores.append(-1)
        return sum(answer_scores)


@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    instance = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        Profile.objects.create(user=instance)


class Question(Model):
    asker = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def sorted_answers(self):
        answers = self.answer_set.all()
        return sorted(answers, key=lambda x: x.answer_score, reverse=True)

    def __str__(self):
        return self.title


class Answer(Model):
    question_answered = models.ForeignKey(Question)
    answerer = models.ForeignKey(User)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_answered.title

    @property
    def voters(self):
        return [vote.voter for vote in self.vote_set.all()]

    @property
    def upvotes(self):
        return self.vote_set.filter(type='up').count()

    @property
    def downvotes(self):
        return self.vote_set.filter(type='down').count()

    @property
    def answer_score(self):
        return self.upvotes - self.downvotes

    @property
    def user_score(self):
        upscore = self.upvotes * 10
        downscore = self.downvotes * -5
        return upscore + downscore


class Tag(Model):
    title = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Vote(Model):
    type = models.CharField(max_length=6, choices=[('up', 'Up'), ('down', 'Down')])
    voter = models.ForeignKey(User)
    answer_voted = models.ForeignKey(Answer)
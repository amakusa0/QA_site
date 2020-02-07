from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    username = models.CharField(max_length=150)
    pub_date = models.DateTimeField('datepublished', default=timezone.now)
    numAnswer = models.IntegerField(default=0)
    isSolved = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.title



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    pub_date = models.DateTimeField('datepublished', default=timezone.now)
    text = models.CharField(max_length=1000)
    votes = models.IntegerField(default=0)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    question_votes = models.IntegerField(default=0)
    answer_votes = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

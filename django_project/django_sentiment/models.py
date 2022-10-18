from email.policy import default
from statistics import mode
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Tweet(models.Model):

    name = models.CharField(max_length=100)
    text = models.TextField()#contenuto del post
    sign = models.CharField(max_length=100, default='neutral')
    polarity = models.CharField(max_length=100, default=0)
    location = models.CharField(max_length=500)
    verified = models.BooleanField()
    retweet = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    account = models.CharField(max_length=500)
    candidate = models.CharField(max_length=500)


    def __str__(self):
        return self.name



class TwitterPolarity(models.Model):

    polarity = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    account = models.CharField(max_length=500)
    sign = models.CharField(max_length=500, default='positive')

    def __str__(self):
        return str(self.id)

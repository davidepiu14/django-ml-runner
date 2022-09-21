from statistics import mode
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Tweet(models.Model):

    name = models.CharField(max_length=100)
    text = models.TextField()#contenuto del post
    sentiment = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    verified = models.BooleanField()
    retweet = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    account = models.CharField(max_length=500)
    sentiment = models.TextField()


    def __str__(self):
        return self.title

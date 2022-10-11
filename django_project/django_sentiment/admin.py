from django.contrib import admin
from django_sentiment.models import Tweet, TwitterPolarity


admin.site.register(Tweet)
admin.site.register(TwitterPolarity)

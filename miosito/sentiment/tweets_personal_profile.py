import csv
import re
import tweepy
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from tweepy import OAuthHandler
import pandas as pd
from credentials import TWITTER_ACCESS_TOKEN, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY

auth = OAuthHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET
)

auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)


api = tweepy.API(auth)

#stuff = api.user_timeline(screen_name = 'danieltosh', count = 100, include_rts = True)


# for status in tweepy.Cursor(api.user_timeline, screen_name='@realDonaldTrump', tweet_mode="extended").items():
#     if (not status.retweeted) and ('RT @' not in status.full_text):
#         print(status.full_text)

for status in tweepy.Cursor(api.user_timeline, id="@realDonaldTrump").items():
    if (not status.retweeted) and ('RT @' not in status.text):
        print(status.text)
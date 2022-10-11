import imp
import pandas as pd
import logging
import re
import os
import tweepy
import logging
import ast
import numpy as np

from dotenv import load_dotenv
from textblob import TextBlob
from tweepy import OAuthHandler

from django_sentiment.models import Tweet, TwitterPolarity



class TwitterScraper:

    config = {}
    load_dotenv()


    def __init__(self):

        self.config['twitter'] = {
            "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
            "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
            "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
            "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        }
        
        self.config['db'] = {
            'db_path':  os.getenv("DB_PATH")
        }

        auth = OAuthHandler(
            self.config['twitter']['consumer_key'],
            self.config['twitter']['consumer_secret'],
        )

        auth.set_access_token(
            self.config['twitter']['access_token'],
            self.config['twitter']['access_token_secret']
        )
        
        self.config['twitter']['twitterAPI'] = tweepy.API(
           auth,
           wait_on_rate_limit = True,
        )


    def clean_tweet_text(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(https?\S+)", " ", tweet).split())


    def get_tweet_sentiment(self, tweet):
        '''
        Comput sentiment with TextBlog
        @return: polarity
        '''
        text = self.clean_tweet_text(tweet)
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return {'sign': 'positive', 'polarity': analysis.sentiment.polarity}
        elif analysis.sentiment.polarity == 0:
            return {'sign': 'neutral', 'polarity': analysis.sentiment.polarity}
        else:
            return {'sign': 'negative', 'polarity': analysis.sentiment.polarity}


    def get_tweets_sentiment(self, query, count=10):
        """
        Return tweet sentiment given a query, it return 10 tweets per page, 
        a mix beetween most populars and recents tweets
        @return: 
        """
        tweets_list = []
        try:
            fetched_tweets = tweepy.Cursor(
                self.config['twitter']['twitterAPI'].search_tweets, 
                q=query, 
                lang="en",
                tweet_mode='extended'
            ).items(count)
            for tweet in fetched_tweets:
                parsed_tweet = {
                    'text': tweet.full_text,
                    'name': tweet.user.name,
                    'location': tweet.user.location,
                    'verified': True if tweet.user.verified else False,
                    'retweet': tweet.retweet_count,
                    'date_tweet': tweet.created_at,
                    'sentiment': str(self.get_tweet_sentiment(tweet.full_text))
                }
            if tweet.retweet_count > 0:
                if parsed_tweet['text'] not in tweets_list:
                    tweets_list.append(parsed_tweet)
            
            return tweets_list
        
        except Exception as e:
            print("Error : %s" % str(e))


    def db_save_tweets(self, query, count):
        """
        get tweets sentiment and save tweet result inside django db
        @return: dict
        """
        res = {}
        tweets = pd.DataFrame(
            self.get_tweets_sentiment(
                query=query,
                count=count
            )
        )
        tweets['candidate'] = query

        try:
            for tweet in tweets.itertuples():
                Tweet.objects.create(
                    name=tweet.name,
                    text=tweet.text,
                    sentiment=tweet.sentiment,
                    location=tweet.location,
                    verified=tweet.verified,
                    retweet=tweet.retweet,
                    date=tweet.date_tweet,
                    account=tweet.name,
                    candidate=tweet.candidate
                )
            res['result'] = 'OK'
        except Exception as ex:
            print("Error: %s" % (ex))
            res['result'] = 'KO'
        
        return res['result']
    

    def pre_process_tweets(self, df_tweets):
        """
        Pre process tweets dataframe
        :return: dataframe
        """
        df_tweets = df_tweets[df_tweets['text']!="text"]
        df_tweets['text'] = df_tweets['text'].apply(self.clean_tweet_text)
        df_tweets = df_tweets.loc[2:]
        df_tweets = df_tweets.dropna(thresh=3)
        df_tweets = df_tweets[df_tweets['sentiment'].str.startswith('{')]
        df_tweets['sentiment'] = df_tweets['sentiment'].apply(ast.literal_eval)
        df_tweets = pd.concat([df_tweets.drop(['sentiment'], axis=1), df_tweets['sentiment'].apply(pd.Series)], axis=1)
        return df_tweets 
    

    def get_all_tweets_from_db(self):
        """
        get tweets from django db
        @return: dataframe
        """
        return pd.DataFrame(
            Tweet.objects.all().values()
        )

    
    def compute_time_series_tweets(self):
        """
        Compute time series tweets
        @return: dataframe
        """
        df_tweets = self.get_all_tweets_from_db()
        df_tweets = self.pre_process_tweets(df_tweets)
        df_tweets['date_tweet'] = pd.to_datetime(df_tweets['date'],errors='coerce').dt.date
        df_tweets['date_tweet'] = pd.to_datetime(df_tweets['date'],errors='coerce').dt.date
        df_tweets = df_tweets.groupby(["candidate", "date"]).aggregate({"polarity":np.mean})

        return pd.DataFrame(df_tweets).reset_index()


    def db_save_tweet_polarity_point(self, df):
        """
        Save time series tweets inside django db
        @return: dict
        """
        res = {}
        try:
            for tweet in df.itertuples():
                TwitterPolarity.objects.create(
                    account=tweet.candidate,
                    date=tweet.date,
                    polarity=tweet.polarity,
                )
            res['result'] = 'OK'
        except Exception as ex:
            print("Error: %s" % (ex))
            res['result'] = 'KO'
        
        return res['result']



if __name__ == "__main__":  
    tw = TwitterScraper()
    tw.db_save_tweets("donald trump", 500) 
    tw.db_save_tweets("joe biden", 500) 

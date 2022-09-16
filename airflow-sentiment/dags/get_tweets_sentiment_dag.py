import pandas as pd
import csv
import re
import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler



from airflow.utils import timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

# GLOBALS
TWITTER_CONSUMER_KEY = Variable.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = Variable.get("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = Variable.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = Variable.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = OAuthHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET
)

auth.set_access_token(
    TWITTER_ACCESS_TOKEN, 
    TWITTER_ACCESS_TOKEN_SECRET
)

twitterAPI = tweepy.API(
    auth,
    wait_on_rate_limit = True ,
)

default_args = {
    'start_date': timezone.datetime(2020, 1, 1),
}



def get_tweets_data(query="Joe Biden", count=10):
    """
    Get tweets data from twitter api
    """
    tweets_list = []
    try:
        fetched_tweets = tweepy.Cursor(
            twitterAPI.search_tweets, 
            q=query, 
            lang="en", 
            tweet_mode='extended'
        ).items(count)
        for tweet in fetched_tweets:
            parsed_tweet = {
                'text': tweet.full_text,
                'name': tweet.user.name,
                'location': tweet.user.location,
                'verified': tweet.user.verified,
                'retweet': tweet.retweet_count,
                'date_tweet': tweet.created_at,
            }
            print(tweet.full_text)
            if tweet.retweet_count > 0:
                if parsed_tweet['text'] not in tweets_list:
                    tweets_list.append(parsed_tweet)
            else:
                tweets_list.append(parsed_tweet)
    
    except Exception as e:
        print("Error : %s" % str(e))
    
    return True


def get_tweets_sentiment(ti, **kwargs):
    """
    """
    
    return True


def do_store_sentiment(ti, **kwargs):

    return True


with DAG(
        'get_tweets_sentiment_dag',
        schedule_interval='@hourly',
        default_args=default_args,
        max_active_runs=1,
        catchup=True
    ) as dag:


    tweets_data = PythonOperator(
        task_id='get_data',
        python_callable=get_tweets_data,
        do_xcom_push=True
    )
    
    # sentiment = PythonOperator(
    #     task_id='sentiment',
    #     python_callable=get_tweets_sentiment,
    #     do_xcom_push=True
    # )

    # store_data_sentiment = PythonOperator(
    #     task_id='store_data',
    #     python_callable=do_store_sentiment,
    #     do_xcom_push=True
    # )


    tweets_data #>> sentiment >> store_data_sentiment
    
import time

from celery import shared_task
from sentiment.scrape_and_save_tweets import dump_tweets
from django.core.cache import cache


@shared_task
def save_tweets(candidate):
    """
    Save tweets into csv
    """
    return dump_tweets(candidate, 50)


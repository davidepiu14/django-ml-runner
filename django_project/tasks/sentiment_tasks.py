import time
import logging
import pandas as pd

from celery import shared_task
from sentiment.scrape_and_save_tweets import dump_tweets
from django.core.cache import cache

_logger = logging.getLogger(__name__)

@shared_task
def save_tweets(candidate):
    """
    Save tweets into csv
    """
    res = {}
    try:
        res['data'] = dump_tweets(candidate, 50),
        res['result'] = 'OK'
    except Exception as ex:
        print("Error: %s" % (ex))
        res['result'] = 'OK'

    return res['result']


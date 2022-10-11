import time
import logging
import pandas as pd

from celery import shared_task
from django.core import management
from django.core.management.commands import loaddata


_logger = logging.getLogger(__name__)

@shared_task
def save_tweets(candidate):
    """
    Save tweets inside SQLite db
    """
    res = {}
    try:
        management.call_command('scrape_tweets', '--query', candidate, '--count', 300)
        res['result'] = 'OK'
    except Exception as ex:
        print("Error: %s" % (ex))
        res['result'] = 'OK'

    return res['result']


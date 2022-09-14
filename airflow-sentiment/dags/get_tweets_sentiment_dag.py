import pandas as pd



from airflow.utils import timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

# GLOBALS
TWITTER_CONSUMER_KEY = Variable.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = Variable.get("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = Variable.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = Variable.get("TWITTER_ACCESS_TOKEN_SECRET")


print(TWITTER_ACCESS_TOKEN)

default_args = {
    'start_date': timezone.datetime(2020, 1, 1),
}


def get_tweets_data(ti, **kwargs):
    """
    Get 3pl deliveries data
    """
   
    return True


def get_tweets_sentiment(ti, **kwargs):
    """
    Change the status order to [handling].
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
    
    sentiment = PythonOperator(
        task_id='sentiment',
        python_callable=get_tweets_sentiment,
        do_xcom_push=True
    )

    store_data_sentiment = PythonOperator(
        task_id='store_data',
        python_callable=do_store_sentiment,
        do_xcom_push=True
    )


    tweets_data >> sentiment >> store_data_sentiment
    
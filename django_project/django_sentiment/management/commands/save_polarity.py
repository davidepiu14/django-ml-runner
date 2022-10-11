from django.core.management.base import BaseCommand, CommandError
from django_sentiment.models import Tweet, TwitterPolarity
from django_sentiment.management.commands._private import TwitterScraper


class Command(BaseCommand):
    
    help = "Save tweets polarity!"

    def handle(self, *args, **options):

        try:
            tw = TwitterScraper()
            df_tweets_time_series = tw.compute_time_series_tweets()
            print(tw.db_save_tweet_polarity_point(df_tweets_time_series))
            self.stdout.write(self.style.SUCCESS('Successfully saved tweets polarity!'))
        
        except Exception as ex:
                print("Error: %s" % (ex))
                self.stdout.write(self.style.ERROR('Error saving tweets polarity!'))

        
        

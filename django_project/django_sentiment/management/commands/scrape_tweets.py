from django.core.management.base import BaseCommand, CommandError
from django_sentiment.models import Tweet, TwitterPolarity
from ._private import TwitterScraper


class Command(BaseCommand):
    
    help = "Scrape tweets from twitter!"

    def add_arguments(self, parser):

        parser.add_argument('--query', nargs='+', type=str)
        parser.add_argument('--count', nargs='+', type=int)

    def handle(self, *args, **options):

        tw = TwitterScraper()
        
        try:
            query = options['query'][0]
        except:
            raise CommandError('Enter a query')
        
        try:
            count = int(options['count'][0])
        except:
            raise CommandError('Enter an integer greater than 0')
        
        if count:
            if count <= 0:
                raise CommandError('Enter an integer greater than 0')
            else:
                tw.db_save_tweets(query, count)
        else:
            tw.db_save_tweets(query, count)

        self.stdout.write(self.style.SUCCESS('Successfully saved tweets for query:  "%s"' % query))
        

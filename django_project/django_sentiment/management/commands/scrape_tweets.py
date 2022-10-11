import imp
from django.core.management.base import BaseCommand, CommandError
from django_sentiment.models import Tweet, TwitterPolarity

class Command(BaseCommand):
    help = "Scrape tweets from twitter!"

    def add_arguments(self, parser):

        parser.add_argument('--query', nargs='+', type=str)
        parser.add_argument('--count', nargs='+', type=int)

    def handle(self, *args, **options):
        

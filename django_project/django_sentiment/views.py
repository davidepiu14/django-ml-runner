import imp
from django.http import HttpResponse
# Create your views here.


def index(self):
    return HttpResponse("Hello django sentiment!")

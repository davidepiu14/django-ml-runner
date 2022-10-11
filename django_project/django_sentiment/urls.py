import imp
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dahsboard_sentiment, name='blog-dashboard'),#path della dashboard
]
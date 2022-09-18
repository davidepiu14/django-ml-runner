# django-airflow-sentiment-twitter

[![Django CI](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml)

This project purpose is to be an example for putting into production ML nlp based algorithms. This is what the django app does:
- fetch tweets data from Twitter API
- process data and classify them and store results in csv format
- results are shown inside a django template throw graphs and one table


### Directories
- core: under this folder we have the django project
- airflow-sentiment: airflow directory (wip), all the fetching/processing phase will be handled with airlfow


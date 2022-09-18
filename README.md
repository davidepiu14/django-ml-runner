# django-ml-runner

[![Django CI](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml) [![Pylint](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml)

## Description
Put into production Machine Lerning models is a complex challenge. Fot this reason I've created this project, the project goal is not to solve any particular architectural problem or is aimed to be the next cutting-edge tool in Machine Learning but to experiment and solve a restricted set of problems using and expanding my expertise. 

At the moment we have a django app that:
- Fetch tweets data from Twitter API
- Process data and classify them and store results in csv format
- It shows the results with a dashboard build with Django's template engine and Highcharts.

## Features I want to build:
- [ ] Run Python Script from Web Client (using Celery) [DOING]
- [ ] Portfolio page
- [X] Blog section

### Directories
- core: under this folder we have the django project
- airflow-sentiment: airflow directory (wip), all the fetching/processing phase will be handled with airlfow


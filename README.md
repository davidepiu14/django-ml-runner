# django-ml-executor

[![Django CI](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml) [![Pylint](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml)

## Description
Often a ML projecs is a data pipeline who begin with source raw data from csv or api and end with the ML model exposed as an api or through a web interface. Put into production Machine Lerning models is a complex challenge. Fot this reason I've created this project, the project goal is not to solve any particular architectural problem or is aimed to be the next cutting-edge tool in Machine Learning, indeed this want to be an experiment to solve a restricted set of problems using and expanding my skills. For now I'm using this technogies to solve diffents problems:
- **Django**: For backend and as a template engine
- **Celery**: As a worker for execute several Python scripts for fetch, process and apply Ml models
- **Redis**: As a task broker and for store tasks results
- **Airflow**: To fetch, process and save data automatically using Airflow DAGs
- **Docker**: To containerize Django and Aiflow

The **Airflow** part is not covered, in the repository you can find only an attempt of a DAG creation. 

At the moment we have a django app that:
- Fetch tweets data from Twitter API
- Process data and classify them and store results in csv format
- It shows the results with a dashboard build with Django's template engine and Highcharts.

## Under development:
- [ ] Run Python Script from Web Client (using Celery) [DOING]
- [ ] Portfolio page
- [X] Blog section

## Folders structure
- ``django_project/``: under this folder we have the django project
- ``airflow_sentiment/``: airflow directory




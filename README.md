# django-ml-executor

[![Django CI](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml) [![Pylint](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml)

## Description
Often a ML projecs is a data pipeline who begin with source raw data from csv or api and end with the ML model exposed as an Api or through a Web interface. Put into production Machine Lerning models is a complex challenge. Fot this reason I've created this project, the project goal is not to solve any particular architectural problem or is aimed to be the next cutting-edge tool in Machine Learning, indeed this want to be an experiment to solve a restricted set of problems using and expanding my skills. For now I'm using this technogies to solve diffents problems:
- **Django**: For backend and as a template engine
- **Celery**: To execute a Python script that fetch twitter data and return the sentiment asynchronally 
- **Airflow**: To fetch, process and save data using Airflow DAGs
- **Docker**: To containerize Django and Aiflow

The **Airflow** part is not covered, in the repository you can find only a first attempt of a DAG creation. 

At the moment we have a django app that:
- Fetch tweets data from Twitter API
- Process data and classify them and store results in csv format
- It shows the results with a dashboard build with Django's template engine and Highcharts.

## Under development:
- [ ] Run Python Script from Web Client (using Celery) [DOING]
- [ ] Portfolio page
- [X] Blog section

### Directories
- core: under this folder we have the django project
- airflow-sentiment: airflow directory (wip), all the fetching/processing phase will be handled with airlfow


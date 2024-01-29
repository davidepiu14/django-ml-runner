# django-ml-runner

[![Django CI](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/django.yml) [![Pylint](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml/badge.svg)](https://github.com/davidepiu14/django-airflow-sentiment/actions/workflows/pylint.yml)

## Description
Often, an ML project is a data pipeline that begins with sourcing raw data from CSV or API and ends with the ML model exposed as an API or through a web interface. Putting Machine Learning models into production is a challenging task. For this reason, I've created this project. The project's goal is not to solve any particular architectural problem or to be the next cutting-edge tool in Machine Learning. Instead, it aims to be an experiment to solve a restricted set of problems using and expanding my skills. Currently, I'm using these technologies:
- **Django**: For backend and as a template engine
- **Celery**: Worker
- **Redis**: Task broker and to store task results
- **Airflow**: To fetch, process, and save data automatically using Airflow DAGs
- **Docker**: To containerize Django and Airflow

The **Airflow** part is not covered. Inside the repository, you can find a first draft of a DAG.

At the moment, we have a Django app that:
- Fetches tweet data from the Twitter API
- Processes data and classifies them, storing results in CSV format
- Displays the results within a dashboard built with Django's template engine and Highcharts.

## Under development
- [X] Run Python Script from Web Client (using Celery)
- [X] Blog section
- [X] Store data into a DBMS

## Folders structure
- `django_project/`: Django web app with sentiment analysis code
- `airflow_sentiment/`: Airflow directory; Python code for DAGs will be under the `dag` folder in the future. For now, you can find a first draft.

## Use cases I would like to cover
- Automate simple tasks like scraping data from common sources like LinkedIn, Wikipedia, etc.
- Automate running simple and well-performing models that don't require a super complex architecture

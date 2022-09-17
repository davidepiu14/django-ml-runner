# /bin/bash

docker build . --tag django-sentiment-airflow:2.3.0
echo "AIRFLOW_IMAGE_NAME=django-sentiment-airflow:2.3.0" >> .env
docker-compose up airflow-init > /dev/null
docker-compose up -d
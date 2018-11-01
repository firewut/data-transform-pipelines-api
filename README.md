# About

Data Transformation Pipelines API.


# Documentation

Documentation available after a startup under [http://127.0.0.1:8000/api/v1/free/docs/](http://127.0.0.1:8000/api/v1/free/docs/)


# Startup

```bash
pip install -r requirements.txt

cd src 
./manage.py migrate
./manage.py runserver 8000
```

Then Execute Redis and Celery

```bash
redis-server

celery -A core worker -l info --concurrency 8 --max-tasks-per-child 2
```
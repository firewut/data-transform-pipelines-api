[![Build Status](https://travis-ci.com/firewut/data-transform-pipelines-api.svg)](https://travis-ci.com/firewut/data-transform-pipelines-api)
[![license](http://img.shields.io/badge/license-MIT-red.svg?style=flat)](https://raw.githubusercontent.com/firewut/data-transform-pipelines-api/master/LICENSE)


# About

Data Transformation API.

Basic Pipeline of Transformation may look like:

  * Receive an Image
    * Resize Image to 500x500
    * Add Watermark to Image using URL or Base64 Image as a **watermark**
    * Grayscale Image
    * Notify any HTTP Service about result completion

## API Documentation

API Documentation available after a startup under [http://127.0.0.1:8000/api/v1/free/docs/](http://127.0.0.1:8000/api/v1/free/docs/)


## Execution

```bash
pip install -r requirements.txt

mkdir ./media
cd src 
./manage.py migrate
./manage.py runserver 8000
```

Then Execute Redis and Celery

```bash
redis-server

celery -A core worker -l info --concurrency 8 --max-tasks-per-child 2
```
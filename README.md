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

## Requirements

Every Worker may have it's own requirements. By default this package requires:

* Libmagic = Required
* OpenCV 3+ - Optional ( used by `template_match_image` processor )

## Execution

Using docker-compose: Starts Queue, Database, Workers and API Itself

```
docker-compose up

# curl -X GET http://127.0.0.1:8000/api/
```

or 

```bash
pip install -r requirements.txt

mkdir ./media ./logs
cd src 
./manage.py migrate
./manage.py collectstatic
./manage.py sync_processors
env DEBUG=True ./manage.py runserver 8000
```

Then Execute Redis and Celery

```bash
redis-server

celery -A core worker -l info --concurrency 8 --max-tasks-per-child 2
```
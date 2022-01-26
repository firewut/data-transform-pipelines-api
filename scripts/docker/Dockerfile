FROM python:3.8

RUN pip3 install -U pip

RUN apt-get update && apt-get upgrade -y
RUN apt-get install uwsgi-plugin-python3 python3-opencv -y

ADD . /project
WORKDIR /project
RUN rm -rf media logs var static && \
    mkdir -p media logs var static
RUN pip3 install --no-cache-dir .

RUN chown -R www-data:www-data /project
USER www-data
WORKDIR /project/src
RUN python3 manage.py collectstatic
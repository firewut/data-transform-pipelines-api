FROM python:3.6

RUN pip3 install -U pip

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python-opencv uwsgi-plugin-python -y

ADD . /project
WORKDIR /project
RUN rm -rf media logs var static && \
    mkdir -p media logs var static
RUN pip3 install -r requirements.txt --no-cache-dir 

RUN chown -R www-data:www-data /project
USER www-data
WORKDIR /project/src
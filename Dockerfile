# pull official base image
FROM python:3.8.3-alpine

# set work directory
RUN mkdir -p /usr/src/tweetme2-project
WORKDIR /usr/src/tweetme2-project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# make pipenv install to the system
ENV PIPENV_SYSTEM=1

# install psycopg2 and Pillow dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev  \
    && apk add zlib-dev jpeg-dev
# ENV LIBRARY_PATH=/lib:/usr/lib

# install dependencies
RUN pip install --upgrade pip pipenv
COPY ./Pipfile ./Pipfile.lock /usr/src/tweetme2-project/
# COPY ./requirements-dev.txt /usr/src/tweetme2/requirements-dev.txt
# RUN pip install -r requirements-dev.txt
# RUN pipenv install Pillow 
RUN pipenv install --deploy
RUN which django-admin

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/tweetme2-project/entrypoint.sh
RUN chmod +x /usr/src/tweetme2-project/entrypoint.sh

# copy project
COPY . /usr/src/tweetme2-project/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/tweetme2-project/entrypoint.sh"]

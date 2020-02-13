# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8-alpine
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
# Set the working directory to /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
# Install any needed packages specified in requirements.txt
RUN apk add --no-cache --virtual .build-deps build-base bash git gcc musl-dev libffi-dev \
 g++ libgcc libstdc++ libxml2-dev libxslt-dev openssl-dev curl \
 && apk add --no-cache --virtual --update-cache\
 jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
 mariadb-dev mariadb-connector-c mariadb-connector-c-dev mariadb-client \
 && pip install -U pip && pip install cython && pip install -r requirements.txt
 COPY . /code
 EXPOSE 8001
 # Make alpine lighter
RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*
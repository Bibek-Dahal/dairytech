# pull official base image
FROM python:3.11.5

# crate directory
RUN mkdir /home/djproj

# set work directory
WORKDIR /home/djproj
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

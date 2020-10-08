FROM python:3.8-slim-buster
WORKDIR /usr/src/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/api/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy
COPY . /usr/src/api/
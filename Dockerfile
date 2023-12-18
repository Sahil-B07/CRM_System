FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN chmod +x /app/django.sh

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"]

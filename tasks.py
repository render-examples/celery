import os
from celery import Celery

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))


@app.task
def add(x, y):
    return x + y

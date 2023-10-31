import json
import logging
import os
import uuid
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_task_logger(__name__)
# Configure the logs
logging.basicConfig(filename='tasks.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#CELERY_BROKER_URL=os.environ.get("CELERY_BROKER_URL")
CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")

try:
    celery = Celery('tasks', broker=CELERY_BROKER_URL)
    logging.info(f'Connecting to Redis CELERY_BROKER_URL: {CELERY_BROKER_URL}')
except Exception as e:
    logging.error(f'Error connecting to Redis CELERY_BROKER_URL: {CELERY_BROKER_URL}. Exception: {e}')
    raise






@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 2})
def add_task(json_data):
    #file_name should be unique, use uuid to generate unique file name
    file_name='jobs/'+uuid.uuid4().hex+'.json'

    with open(file_name, 'w') as file:
        json.dump(json_data, file)

    logging.info(f'Job {file_name} added to queue')

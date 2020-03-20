import os
from celery import Celery
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition)
from sendgrid import SendGridAPIClient
from uuid import uuid4
import csv

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379"))


@app.task
def bulk_predict(model, data, email):

    predictions = model.predict(data)[0].tolist()

    message = Mail(
        from_email='thilo@colabel.com',
        to_emails=email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    filename = str(uuid4()) + '.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['text', 'label'])
        for text, prediction in zip(data, predictions):
            writer.writerow([text, prediction])

    with open(filename, 'rb') as f:
        data = f.read()
        f.close()

    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/csv')
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition('attachment')
    message.attachment = attachment

    client = SendGridAPIClient(os.getenv("SENDGRID_KEY"))
    client.send(message)

    os.remove(filename)

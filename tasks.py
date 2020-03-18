import os
from celery import Celery
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient


app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))


@app.task
def add(x, y):
    return x + y


@app.task
def bulk_predict(data=['i like', 'i hate'], email):


    message = Mail(
        from_email='thilo@colabel.com',
        to_emails=email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    file_path = 'example.pdf'
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()

    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName('test_filename.pdf')
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('Example Content ID')
    message.attachment = attachment

    sendgrid_client = SendGridAPIClient('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')
    response = sendgrid_client.send(message)
    print(response)
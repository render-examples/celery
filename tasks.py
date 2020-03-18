import os
from celery import Celery
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient

message = Mail(
    from_email='from_email@example.com',
    to_emails='to@example.com',
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
try:
    sendgrid_client = SendGridAPIClient('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')
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))


@app.task
def add(x, y):
    return x + y


@app.task
def bulk_predict(csv_file, email):


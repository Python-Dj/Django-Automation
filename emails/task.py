from AUTODjango.celery import app
from dataentry.utils import send_email_notification


@app.task
def send_emails_task(mail_subject, message, to_email, attachment):
    send_email_notification(mail_subject, message, to_email, attachment)
    return "Emails sending task completed Successfully!"
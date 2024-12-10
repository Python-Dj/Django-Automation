import time

from django.core.management import call_command
from AUTODjango.celery import app
from dataentry.utils import send_email_notification



@app.task
def import_data_task(file_path, model_name):
    #! Now here we call the our importdata command.
    try:
        call_command("importdata", file_path, model_name)
    except Exception as e:
        raise e
    
    #! notify to user by email.
    mail_subject = "Import Data Completed!"
    message = "Your data has been imported Successfully!"
    to_email = 'handsomearjun360@gmail.com'
    send_email_notification(mail_subject, message, to_email)

    return "Data Imported Successfully!"

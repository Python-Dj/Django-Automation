import time

from django.core.management import call_command
from AUTODjango.celery import app
from dataentry.utils import send_email_notification, generate_csv_file



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
    send_email_notification(mail_subject, message, [to_email])

    return "Data Imported Successfully!"


@app.task
def export_data_task(model_name):
    try:
        call_command("exportdata", model_name)
    except Exception as e:
        raise e
    
    file_path = generate_csv_file(model_name)

    #! send email with attachment.
    mail_subject = "Export Data Completed!"
    message = "Data exported Successfully! Find the attachment File."
    to_email = "handsomearjun360@gmail.com"
    send_email_notification(mail_subject, message, [to_email], attachment=file_path)
    return "Your Data is Exported!!"
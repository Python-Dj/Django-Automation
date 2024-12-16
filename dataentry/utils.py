import csv
import os
import hashlib
import time

from datetime import datetime
from django.db import DataError
from django.core.management.base import CommandError
from django.apps import apps
from django.core.mail import EmailMessage
from django.conf import settings
from bs4 import BeautifulSoup

from emails.models import Email, Sent, EmailTracking, Subscriber

#| only list those that are created by the developer or owner.
def get_custom_models():
    default_models = ["ContentType", "Session", "LogEntry", "Group", "Permission", "Upload"]

    #! filtering the custom model.
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models


def check_csv_errors(file_path, model_name):
    #| Search for the model accross all installed apps.
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break # stop searching once model is found.
        except LookupError:
            continue # continue searching if model is not found.
    
    if not model:
        raise CommandError(f"'{model_name}' Model is not found!")
    
    #! compare the csv_file header with model fields.
    #! get all the fields of model except 'id' field.
    model_fields = [field.name for field in model._meta.fields if field.name != "id"]
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_headers = reader.fieldnames
            if model_fields != csv_headers:
                raise DataError(f"CSV file doesn't match with {model_name} tables field.")
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email:
            # Create Email tracking record
            new_message = message
            if email_id:
                email = Email.objects.get(id=email_id)
                subscriber = Subscriber.objects.get(email_address=recipient_email)
                
                #! Creating unique id.
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id
                )

                # Generate the tracking pixel
                base_url = settings.BASE_URL
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

                # Searchfor the link in email body
                soup = BeautifulSoup(message, "html.parser") 
                urls = [a["href"] for a in soup.find_all("a", href=True)]

                # If there are links or urls in the email body, inject our click tracking url to the original link.
                if urls:
                    for url in urls:
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")

                #Note: Create the email content with tracking pixel image.
                open_tracking_img = f"<img src='{open_tracking_url}' width='1', height='1'>"
                new_message += open_tracking_img

            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])
            if attachment is not None:
                mail.attach_file(attachment)
            mail.content_subtype = "html"
            mail.send()

        #! Here we r storing the email sent to how many subscribers.
        if email_id: 
            total_sent = email.email_list.count_emails()
            Sent.objects.create(email=email, total_sent=total_sent)
    except Exception as e:
        raise e
    

def generate_csv_file(model_name):
    #| Get current timestamp.
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f"export_{model_name}_{timestamp}.csv"

    attached_dir = "export_data"
    file_path = os.path.join(settings.MEDIA_ROOT, attached_dir, file_name)
    return file_path
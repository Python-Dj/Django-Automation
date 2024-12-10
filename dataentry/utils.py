import csv

from django.db import DataError
from django.core.management.base import CommandError
from django.apps import apps
from django.core.mail import EmailMessage
from django.conf import settings


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


def send_email_notification(mail_subject, message, to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e
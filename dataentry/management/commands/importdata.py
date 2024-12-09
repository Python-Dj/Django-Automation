from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DataError

from dataentry.models import Student
import csv



class Command(BaseCommand):
    help = "Import data from csv file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="path to the csv file")
        parser.add_argument("model_name", type=str, help="model name")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        model_name = options["model_name"].capitalize()

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
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_headers = reader.fieldnames
            if model_fields != csv_headers:
                raise DataError(f"CSV file doesn't match with {model_name} tables field.")
            student_instances = [model(**row) for row in reader]
            model.objects.bulk_create(student_instances)

        self.stdout.write(self.style.SUCCESS("Data imported from CSV Successfully!!"))
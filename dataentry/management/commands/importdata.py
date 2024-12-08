from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

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
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            student_instances = [model(**row) for row in reader]
            model.objects.bulk_create(student_instances)

        self.stdout.write(self.style.SUCCESS("Data imported from CSV Successfully!!"))
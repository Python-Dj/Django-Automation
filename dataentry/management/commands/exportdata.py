import csv

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.apps import apps
from dataentry.utils import generate_csv_file




class Command(BaseCommand):
    help = "Export data in CSV file."

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Model Name")

    def handle(self, *args, **options):
        model_name = options["model_name"].capitalize()

        model = None
        for app_conf in apps.get_app_configs():
            try:
                model =  apps.get_model(app_conf.label, model_name)
                break
            except LookupError:
                continue
        
        if not model:
            raise CommandError(f"There is not model name with '{model_name}'")
        #| Fetch data for the model.
        model_data = model.objects.all()

        file_path = generate_csv_file(model_name)

        with open(file_path, 'w', newline="") as file:
            writer = csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])

            #| Write the Student data in csv file.
            for data in model_data:
                writer.writerow([getattr(data, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS("Data Exported!!!"))

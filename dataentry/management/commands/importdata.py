import csv

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DataError

from dataentry.models import Student
from dataentry.utils import check_csv_errors



class Command(BaseCommand):
    help = "Import data from csv file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="path to the csv file")
        parser.add_argument("model_name", type=str, help="model name")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        model_name = options["model_name"].capitalize()

        model = check_csv_errors(file_path, model_name)

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            student_instances = [model(**row) for row in reader]
            model.objects.bulk_create(student_instances)

        self.stdout.write(self.style.SUCCESS("Data imported from CSV Successfully!!"))
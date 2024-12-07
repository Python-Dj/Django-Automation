from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Greet command"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        
    def handle(self, *args, **options):
        name = options["name"]
        self.stdout.write(self.style.WARNING("This is a Greet Command!!!!"))
        self.stdout.write(self.style.SUCCESS(f"Welcome to Command Section {name}"))
from django.core.management.base import BaseCommand, CommandError

from dataentry.models import Student


#| insert data to database using custom Command.

class Command(BaseCommand):
    help = "It will insert data to database"

    # def add_arguments(self, parser):
    #     parser.add_argument("roll_number", type=str)
    #     parser.add_argument("name", type=str)
    #     parser.add_argument("age", type=int)

    
    def handle(self, *args, **options):
        # Student.objects.create(
        #     roll_number=options["roll_number"],
        #     name=options["name"],
        #     age=options["age"]
        # )

        
        students = [
            {"roll_number": "ER5640", "name": "Keshava", "age": 25},
            {"roll_number": "ER5848", "name": "Bhairava", "age": 55},
            {"roll_number": "ER5353", "name": "Kaal", "age": 38},
            {"roll_number": "ER5742", "name": "Madhava", "age": 93},
            {"roll_number": "ER6142", "name": "Shankara", "age": 93},
        ]

        #| Create data in bulk. First create the instance of all data then insert all at once in database using bulk_Create.
        student_instances = [Student(**student) for student in students if not Student.objects.filter(roll_number=student["roll_number"]).exists()]

        Student.objects.bulk_create(student_instances)
        self.stdout.write(self.style.SUCCESS("Data has been inserted Successfully!!!"))
from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=8)
    name = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(unique=True, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    gpa = models.CharField(max_length=4, blank=True, null=True)
    graduation_year = models.CharField(max_length=4, blank=True, null=True)


    def __str__(self):
        return self.name
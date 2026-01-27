from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.full_name

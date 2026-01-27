from django.db import models

from employees.models import Employee


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        (
            "in_progres",
            "In Progres",
        ),
        ("done", "Done"),
    ]
    name = models.CharField(max_length=255)
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subtasks",
    )
    assignee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name="tasks"
    )
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.name

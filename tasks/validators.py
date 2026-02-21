from datetime import date
from django.core.exceptions import ValidationError
from employees.models import Employee

def validate_due_date(value):
    """Срок задачи не может быть в прошлом"""
    if value < date.today():
        raise ValidationError("Срок задачи не может быть в прошлом.")

def validate_assignee_load(employee: Employee):
    """Проверка, что у сотрудника не слишком много активных задач"""
    active_tasks_count = employee.tasks.exclude(status='done').count()
    MAX_TASKS = 10
    if active_tasks_count >= MAX_TASKS:
        raise ValidationError(f"Сотрудник {employee.full_name} перегружен ({active_tasks_count} активных задач).")

def validate_parent_task(task, parent_task):
    """Если указана родительская задача, она должна быть взята в работу или завершена"""
    if parent_task and parent_task.status not in ['in_progress', 'done']:
        raise ValidationError("Родительская задача должна быть взята в работу или завершена.")

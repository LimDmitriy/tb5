import pytest
from rest_framework.test import APIClient
from employees.models import Employee
from tasks.models import Task
from datetime import date, timedelta

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def employees():
    e1 = Employee.objects.create(full_name="Иван Иванов", position="Разработчик")
    e2 = Employee.objects.create(full_name="Петр Петров", position="Тестировщик")
    return [e1, e2]

@pytest.fixture(autouse=True)
def clear_db():
    Task.objects.all().delete()
    Employee.objects.all().delete()

def test_create_task(api_client, employees):
    e1 = employees[0]
    data = {
        "name": "Новая задача",
        "assignee": e1.id,
        "status": "pending",
        "due_date": str(date.today() + timedelta(days=7))
    }
    response = api_client.post("/tasks/", data)
    assert response.status_code == 201
    assert Task.objects.filter(name="Новая задача").exists()

def test_delete_task(api_client, employees):
    e1 = employees[0]
    task = Task.objects.create(
        name="Задача на удаление",
        assignee=e1,
        status="pending",
        due_date=date.today() + timedelta(days=5)
    )
    response = api_client.delete(f"/tasks/{task.id}/")
    assert response.status_code == 204
    assert not Task.objects.filter(id=task.id).exists()

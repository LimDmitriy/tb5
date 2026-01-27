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

def test_create_employee(api_client):
    data = {"full_name": "Мария Сидорова", "position": "Менеджер"}
    response = api_client.post("/employees/", data)
    assert response.status_code == 201
    assert Employee.objects.filter(full_name="Мария Сидорова").exists()

def test_update_employee(api_client, employees):
    emp = employees[0]
    data = {"full_name": "Иван Иванович", "position": emp.position}
    response = api_client.put(f"/employees/{emp.id}/", data)
    assert response.status_code == 200
    emp.refresh_from_db()
    assert emp.full_name == "Иван Иванович"

def test_delete_employee(api_client, employees):
    emp = employees[0]
    response = api_client.delete(f"/employees/{emp.id}/")
    assert response.status_code == 204
    assert not Employee.objects.filter(id=emp.id).exists()

def test_busy_employees(api_client, employees):
    emp1, emp2 = employees
    Task.objects.create(
        name="Задача 1",
        assignee=emp1,
        status="in_progress",
        due_date=date.today() + timedelta(days=5)
    )
    Task.objects.create(
        name="Задача 2",
        assignee=emp1,
        status="in_progress",
        due_date=date.today() + timedelta(days=3)
    )
    Task.objects.create(
        name="Задача 3",
        assignee=emp2,
        status="pending",
        due_date=date.today() + timedelta(days=4)
    )

    response = api_client.get("/employees/busy/")
    assert response.status_code == 200
    assert response.data[0]["full_name"] == "Иван Иванов"  # больше всего активных задач
    assert response.data[0]["active_tasks_count"] == 2

# Task Tracker

Серверное приложение для трекинга задач сотрудников.

## Установка 

```bash
git clone <репозиторий>
cd tb5
poetry install
cp .env.example .env 
python3 manage.py migrate
python3 manage.py runserver
```

## Docker
```
docker build -t tb5 .
docker run -p 8000:8000 tb5
```

## API
#### CRUD сотрудников
```
GET /employees/ — список сотрудников

POST /employees/ — создать сотрудника

PUT /employees/{id}/ — обновить

DELETE /employees/{id}/ — удалить

CRUD задач

GET /tasks/ — список задач

POST /tasks/ — создать задачу

PUT /tasks/{id}/ — обновить

DELETE /tasks/{id}/ — удалить

Специальные эндпоинты

GET /employees/busy/ — занятые сотрудники

GET /tasks/important/ — важные задачи
```
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Task
from employees.models import Employee
from .serializers import TaskModelSerializer, ImportantTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

    @action(detail=False, methods=['get'])
    def important(self, request):
        """Эндпоинт важные задачи"""
        pending_tasks = Task.objects.filter(status='pending')
        critical_tasks = pending_tasks.filter(subtasks__status='in_progress').distinct()

        emp_load = Employee.objects.annotate(
            active_count=Count('tasks', filter=~Q(tasks__status='done'))
        )
        if not emp_load:
            return Response([])

        min_load_count = min(emp.active_count for emp in emp_load)
        least_busy_emps = [emp for emp in emp_load if emp.active_count == min_load_count]

        result = []

        for task in critical_tasks:
            parent_assignee = []
            if task.parent_task and task.parent_task.assignee:
                parent_emp = task.parent_task.assignee
                if parent_emp.tasks.exclude(status='done').count() <= min_load_count + 2:
                    parent_assignee.append(parent_emp.full_name)

            potential_emps = set(emp.full_name for emp in least_busy_emps) | set(parent_assignee)

            result.append({
                "task": task.name,
                "due_date": task.due_date,
                "potential_employees": list(potential_emps)
            })

        serializer = ImportantTaskSerializer(result, many=True)
        return Response(serializer.data)

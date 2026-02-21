from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Employee
from tasks.models import Task
from .serializers import (
    EmployeeModelSerializer,
    BusyEmployeeSerializer,
    ActiveTaskSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeModelSerializer

    @action(detail=False, methods=['get'])
    def busy(self, request):
        """Эндпоинт занятые сотрудники"""
        employees = Employee.objects.all()
        data = []

        for emp in employees:
            active_tasks = Task.objects.filter(assignee=emp).exclude(status='done')
            data.append({
                "full_name": emp.full_name,
                "position": emp.position,
                "active_tasks_count": active_tasks.count(),
                "tasks": ActiveTaskSerializer(active_tasks, many=True).data
            })

        data.sort(key=lambda x: x['active_tasks_count'], reverse=True)

        serializer = BusyEmployeeSerializer(data, many=True)
        return Response(serializer.data)

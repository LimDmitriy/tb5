from rest_framework import serializers
from .models import Employee
from tasks.models import Task


class ActiveTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "due_date", "status"]


class BusyEmployeeSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    position = serializers.CharField()
    active_tasks_count = serializers.IntegerField()
    tasks = ActiveTaskSerializer(many=True)


class EmployeeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position", "email"]

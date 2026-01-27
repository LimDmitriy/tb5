from rest_framework import serializers
from .models import Task



class ImportantTaskSerializer(serializers.Serializer):
    task = serializers.CharField()
    due_date = serializers.DateField()
    potential_employees = serializers.ListField(child=serializers.CharField())


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'parent_task', 'assignee', 'due_date', 'status']

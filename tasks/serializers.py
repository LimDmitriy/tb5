from rest_framework import serializers
from .models import Task
from .validators import validate_due_date, validate_assignee_load, validate_parent_task


class ImportantTaskSerializer(serializers.Serializer):
    task = serializers.CharField()
    due_date = serializers.DateField()
    potential_employees = serializers.ListField(child=serializers.CharField())

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        """Проверка даты задачи"""
        validate_due_date(value)
        return value

    def validate(self, attrs):
        """Валидация зависимостей между полями"""
        assignee = attrs.get('assignee')
        parent_task = attrs.get('parent_task')
        task = self.instance
        if assignee:
            validate_assignee_load(assignee)
        if parent_task:
            validate_parent_task(task, parent_task)

        return attrs

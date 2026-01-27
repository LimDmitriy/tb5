from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'assignee', 'status', 'due_date', 'parent_task')
    list_filter = ('status', 'due_date')
    search_fields = ('name',)

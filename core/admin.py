from django.contrib import admin
from .models import Task, TaskAssignment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'due_date')
    list_filter = ('status', 'created_by', 'due_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'assigned_to', 'is_completed', 'assigned_at')
    list_filter = ('is_completed', 'assigned_to', 'assigned_at')
    search_fields = ('task__title', 'assigned_to__username')
    readonly_fields = ('assigned_at', 'completed_at') 
# tasks/admin.py
from django.contrib import admin
from .models import Task, UserTask, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'date_of_birth', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'status', 'assigned_at', 'updated_at')
    list_filter = ('status', 'assigned_at', 'updated_at')
    search_fields = ('user__username', 'task__title')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'task')
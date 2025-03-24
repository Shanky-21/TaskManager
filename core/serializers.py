from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, TaskAssignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'updated_at', 
                 'created_by', 'due_date', 'status', 'assigned_users')
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    def get_assigned_users(self, obj):
        return UserSerializer(obj.assignments.values_list('assigned_to', flat=True), many=True).data

class TaskAssignmentSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ('id', 'task', 'assigned_to', 'assigned_at', 'is_completed', 'completed_at')
        read_only_fields = ('id', 'assigned_at') 
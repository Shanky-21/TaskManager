from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task, TaskAssignment
from .serializers import UserSerializer, TaskSerializer, TaskAssignmentSerializer
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            return Task.objects.filter(assignments__assigned_to=user)
        return Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def assign_users(self, request, pk=None):
        task = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        for user_id in user_ids:
            user = get_object_or_404(User, id=user_id)
            TaskAssignment.objects.get_or_create(task=task, assigned_to=user)
        
        return Response({'status': 'users assigned'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        assignment = get_object_or_404(TaskAssignment, task=task, assigned_to=request.user)
        assignment.is_completed = True
        assignment.save()
        return Response({'status': 'task completed'}) 
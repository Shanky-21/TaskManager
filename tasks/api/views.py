# tasks/api/views.py
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.contrib.auth.models import User
from ..models import Task, UserProfile, UserTask
from ..serializers import (
    TaskSerializer, 
    UserSerializer, 
    UserProfileSerializer
)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'uuid'
    
    def perform_destroy(self, instance):
        # Check if the user is the task creator
        if instance.created_by != self.request.user:
            raise PermissionDenied("You can only delete tasks that you created.")
        instance.delete()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        # For DELETE requests, check if user is the creator
        if request.method == 'DELETE' and obj.created_by != request.user:
            raise PermissionDenied("You can only delete tasks that you created.")

    def get_queryset(self):
        queryset = Task.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_assignments__user_id=user_id)
        return queryset

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get tasks assigned to the current user"""
        tasks = Task.objects.filter(user_assignments__user=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def status(self, request, uuid=None):
        """Update status of a task for the current user"""
        task = self.get_object()
        user_task = get_object_or_404(
            UserTask, 
            task=task, 
            user=request.user
        )
        
        new_status = request.data.get('status')
        if new_status not in dict(UserTask.STATUS_CHOICES):
            return Response(
                {'status': ['Invalid status. Choose from: pending, in_progress, completed']}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user_task.status = new_status
        user_task.save()
        
        return Response({
            'uuid': task.uuid,
            'user_task_uuid': user_task.uuid,
            'status': user_task.status,
            'updated_at': user_task.updated_at
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Override to allow unauthenticated access to registration
        """
        if self.action == 'create':  # registration
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
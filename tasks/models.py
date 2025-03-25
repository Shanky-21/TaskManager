# tasks/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class UserProfile(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True, default=generate_uuid, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"

class Task(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True, default=generate_uuid, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        return self.title

    @property
    def assigned_users(self):
        """Get all users assigned to this task"""
        return User.objects.filter(usertask__task=self)

class UserTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    uuid = models.CharField(max_length=36, primary_key=True, default=generate_uuid, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_assignments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='user_assignments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({self.status})"
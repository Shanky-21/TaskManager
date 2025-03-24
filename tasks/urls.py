# tasks/urls.py
from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('task/<uuid:uuid>/', views.task_detail, name='task_detail'),
    # Add these URLs for later implementation
    path('task/create/', views.create_task, name='create_task'), 
    path('task/<uuid:uuid>/edit/', views.edit_task, name='edit_task'),
    path('task/<uuid:uuid>/delete/', views.delete_task, name='delete_task'),
]
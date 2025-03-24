# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Task, UserTask
from .forms import CustomUserCreationForm, TaskForm
from django.contrib.auth.models import User

def hello_world(request):
    return HttpResponse("Hello, World!")
  
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('tasks:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
  
  

@login_required
def edit_task(request, uuid):
    task = get_object_or_404(Task, uuid=uuid)
    
    # Check if user has permission to edit
    if request.user != task.created_by:
        messages.error(request, "You don't have permission to edit this task.")
        return redirect('tasks:task_detail', uuid=uuid)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_detail', uuid=uuid)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task
    })
  

@login_required
def task_detail(request, uuid):
    task = get_object_or_404(Task, uuid=uuid)
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'can_edit': request.user == task.created_by
    })

@login_required
def dashboard(request):
    user_tasks = Task.objects.filter(assigned_users=request.user)
    all_tasks = Task.objects.all()
    users = User.objects.all()
    
    # Filter by user if specified
    filter_user = request.GET.get('user')
    if filter_user:
        all_tasks = all_tasks.filter(assigned_users__id=filter_user)

    context = {
        'user_tasks': user_tasks,
        'all_tasks': all_tasks,
        'users': users,
        'selected_user': filter_user,
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def task_detail(request, uuid):
    task = get_object_or_404(Task, uuid=uuid)
    return render(request, 'tasks/task_detail.html', {'task': task})
  

@login_required
def delete_task(request, uuid):
    task = get_object_or_404(Task, uuid=uuid)
    
    # Check if user has permission to delete
    if request.user != task.created_by:
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('tasks:task_detail', uuid=uuid)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('tasks:dashboard')
    
    return redirect('tasks:task_detail', uuid=uuid)
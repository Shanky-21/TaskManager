# tasks/views.py
import json
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
            task = form.save()
            
            # Update assignments
            new_assignments = json.loads(request.POST.get('assignments', '[]'))
            
            # Delete existing assignments not in the new list
            existing_user_ids = [a['user_id'] for a in new_assignments]
            task.user_assignments.exclude(user_id__in=existing_user_ids).delete()
            
            # Create or update assignments
            for assignment in new_assignments:
                UserTask.objects.update_or_create(
                    task=task,
                    user_id=assignment['user_id'],
                    defaults={'status': assignment['status']}
                )
            
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_detail', uuid=uuid)
    else:
        form = TaskForm(instance=task)
        # Get current assignments for the form
        current_assignments = [
            {
                'user_id': ua.user_id,
                'status': ua.status
            }
            for ua in task.user_assignments.all()
        ]
        form.initial['assignments'] = json.dumps(current_assignments)
    
    context = {
        'form': form,
        'task': task,
        'users': User.objects.all(),
        'status_choices': UserTask.STATUS_CHOICES,
        'current_assignments': task.user_assignments.all()
    }
    return render(request, 'tasks/edit_task.html', context)
  

@login_required
def task_detail(request, uuid):
    task = get_object_or_404(
        Task.objects.prefetch_related('user_assignments', 'user_assignments__user'),
        uuid=uuid
    )
    
    # Get the user's assignment for this task if it exists
    user_task = task.user_assignments.filter(user=request.user).first()
    
    context = {
        'task': task,
        'user_task': user_task,
        'can_edit': request.user == task.created_by,
        'user_assignments': task.user_assignments.all()
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def dashboard(request):
    # Get tasks where the user is assigned
    user_tasks = Task.objects.filter(user_assignments__user=request.user)
    
    # Get all tasks for admin view
    all_tasks = Task.objects.all().prefetch_related('user_assignments', 'user_assignments__user')
    
    # Filter by user if specified
    filter_user = request.GET.get('user')
    if filter_user:
        all_tasks = all_tasks.filter(user_assignments__user_id=filter_user)

    # Get all users for the filter dropdown
    users = User.objects.all()

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
            
            # Handle assignments
            assignments = json.loads(request.POST.get('assignments', '[]'))
            for assignment in assignments:
                UserTask.objects.create(
                    task=task,
                    user_id=assignment['user_id'],
                    status=assignment['status']
                )
            
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'users': User.objects.all(),
        'status_choices': UserTask.STATUS_CHOICES
    }
    return render(request, 'tasks/create_task.html', context)

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
# task_manager_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),   # Keep only this logout URL
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('tasks.urls')),
]
# tasks/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, UserProfile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    
    # Additional fields you might want
    address = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name", 
            "email", 
            "phone",
            "address",
            "date_of_birth",
            "username", 
            "password1", 
            "password2"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"],
                date_of_birth=self.cleaned_data["date_of_birth"]
            )
        return user
      
class TaskForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_users']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'assigned_users': forms.CheckboxSelectMultiple()
        }
        
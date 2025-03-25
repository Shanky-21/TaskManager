# tasks/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserProfile, UserTask

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['uuid', 'phone', 'address', 'date_of_birth', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    phone = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True, required=False)
    date_of_birth = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 
                 'last_name', 'profile', 'phone', 'address', 'date_of_birth')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Extract profile data
        phone = validated_data.pop('phone')
        address = validated_data.pop('address', '')
        date_of_birth = validated_data.pop('date_of_birth', None)

        # Create user
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create user profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            date_of_birth=date_of_birth
        )

        return user
class UserTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserTask
        fields = ['uuid', 'user', 'user_id', 'status', 'assigned_at', 'updated_at']  # Changed 'id' to 'uuid'

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assignments = UserTaskSerializer(source='user_assignments', many=True, read_only=True)
    assign_to = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'uuid',  # Changed 'id' to 'uuid'
            'title', 
            'description', 
            'created_at', 
            'updated_at', 
            'created_by', 
            'assignments',
            'assign_to'
        ]

    def create(self, validated_data):
        assignments = validated_data.pop('assign_to', [])
        # Add created_by from the context
        validated_data['created_by'] = self.context['request'].user
        task = Task.objects.create(**validated_data)
        
        # Create UserTask entries
        for assignment in assignments:
            UserTask.objects.create(
                task=task,
                user_id=assignment['user_id'],
                status=assignment.get('status', 'pending')
            )
          
        return task

    def update(self, instance, validated_data):
        assignments = validated_data.pop('assign_to', [])
        
        # Update task fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update assignments if provided
        if assignments:
            # Get current assignments
            current_assignments = set(instance.user_assignments.values_list('user_id', flat=True))
            new_assignments = set(assignment['user_id'] for assignment in assignments)
            
            # Remove assignments not in the new list
            instance.user_assignments.filter(user_id__in=current_assignments - new_assignments).delete()
            
            # Update or create new assignments
            for assignment in assignments:
                UserTask.objects.update_or_create(
                    task=instance,
                    user_id=assignment['user_id'],
                    defaults={'status': assignment.get('status', 'pending')}
                )

        return instance
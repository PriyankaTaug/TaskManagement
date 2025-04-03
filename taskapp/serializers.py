from rest_framework import serializers
from .models import CustomUser, Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password','role']

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extract password separately
        user = CustomUser(**validated_data)  # Create user without saving
        user.set_password(password)  # Hash password properly
        user.save()  # Save user
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
from dataclasses import fields
from .models import CustomUser as User
# from django.contrib.auth.models import AbstractUser as User
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class UserSerializer(serializers.ModelSerializer):
    #resume = serializers.CharField(source='userprofile.resume')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'cv', 'github', 'linkedin', 'id')
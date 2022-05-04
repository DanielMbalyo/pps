from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'staff', ]

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password',]
        extra_kwargs = {"password": {"write_only": True}}

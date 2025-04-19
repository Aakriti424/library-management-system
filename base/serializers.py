from rest_framework import serializers
from .models import *


#USER SERIALIZER

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model=User
        fields=['username', 'password', 'email', 'role', 'address', 'contact']

    
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role'],
            address=validated_data['address'],
            contact=validated_data['contact']
        )
        return user

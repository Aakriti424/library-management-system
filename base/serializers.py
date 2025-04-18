from rest_framework import serializers
from .models import *


#USER SERIALIZER

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'password', 'email', 'role', 'address', 'contact']

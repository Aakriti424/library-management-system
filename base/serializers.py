from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
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
    

#Books Serializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'


class BorrowingRecordSerializer(serializers.ModelSerializer):
    borrower_name=serializers.SerializerMethodField()
    class Meta:
        model=BorrowingRecord
        fields=['status','borrower', 'borrower_name', 'borrowed_book', 'borrowed_at', 'due_date', 'return_date']
        read_only_fields=['borrower','due_date']

    def get_borrower_name(self, obj):
        return obj.borrower.username

    def create(self, validated_data):
        borrowed_at=timezone.now().date()
        due_date=borrowed_at+timedelta(days=30)
        validated_data['due_date']=due_date
        user=self.context['request'].user
        validated_data['borrower']=user
        return super().create(validated_data)
        


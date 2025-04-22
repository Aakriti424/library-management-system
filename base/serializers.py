from rest_framework import serializers   
from datetime import timedelta
from django.utils import timezone
from .models import *


#USER SERIALIZER

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=6)   #TO MAKE PASSWORD FIELD MORE FLEXIBLE AND REAL
    class Meta:
        model=User
        fields=['username', 'password', 'email', 'role', 'address', 'contact']

    
    def create(self, validated_data):       #TO CREATE THE USER TABLE 
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
        read_only_fields=['borrower','due_date']        #USER CANNOT POST DATAS IN THESE FIELDS WITH THE HELP OF READ ONLY FIELDS


    def get_borrower_name(self, obj):       #HELPS TO DISPLAY THE NAME OF THE USER INSTEAD OF THEIR ID
        return obj.borrower.username

    def create(self, validated_data):
        borrowed_at=timezone.now().date()       #IT IS OPERATED HERE BECAUSE WE NEED HELP OF THIS VAIRABLE TO CREATE DUE DATE
        due_date=borrowed_at+timedelta(days=30)     #TIME DELTA HELPS IN ADDING EXTRA 30 DAYS IN THE CURRENT DAY STORED IN BORROWED_AT VARIABLE
        validated_data['due_date']=due_date
        user=self.context['request'].user
        validated_data['borrower']=user
        return super().create(validated_data)
        


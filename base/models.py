from django.db import models
from django.contrib.auth.models import AbstractUser


#USER MODEL

class User(AbstractUser):

    ROLE_CHOICES=[
        ('management', 'Management'),
        ('member', 'Member')
    ]
    username=models.CharField(max_length=300, unique=True)
    password=models.CharField(max_length=300)
    email=models.EmailField()
    role=models.CharField(max_length=100, choices=ROLE_CHOICES)
    address=models.CharField(max_length=300)
    contact=models.CharField(max_length=300)

 
 
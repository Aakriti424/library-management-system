from django.db import models
from django.contrib.auth.models import AbstractUser


#USER MODEL
class User(AbstractUser):
    ROLE_CHOICES=[
        ('librarian', 'Librarian'),
        ('member', 'Member')
    ]       #CHOICES OF ROLE TO PROVIDE PERMISSIONS 

    username=models.CharField(max_length=300, unique=True)
    password=models.CharField(max_length=300)
    email=models.EmailField()
    role=models.CharField(max_length=100, choices=ROLE_CHOICES)
    address=models.CharField(max_length=300)
    contact=models.CharField(max_length=300)

 
 #Books Model
class Book(models.Model):
    GENRE_CHOICES=[
       ('novel', 'Novel'),
       ('poem', 'Poem'),
       ('story', 'Story')
    ]       #CHOICES FOR USER TO NAVIGATE THROUGH THE LIBRARY DATA EASILY

    title=models.CharField(max_length=300, unique=True)
    author=models.CharField(max_length=300)
    published_date=models.DateField()
    genre=models.CharField(max_length=100, choices=GENRE_CHOICES)

    def __str__(self):      #TO DISPLAY THE NAME OF THE TITLE INSTEAD OF THE OBJECT IN THE ADMIN PANNEL
        return self.title


#RECORD MODEL
class BorrowingRecord(models.Model):
    STATUS_CHOICES=[
        ('returned', 'Returned'),
        ('borrowed', 'Borrowed')
    ]       
    borrower=models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_book=models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at=models.DateField(auto_now_add=True)
    due_date=models.DateField()
    return_date=models.DateField(null=True, blank=True)
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, default='borrowed')
    
    def __str__(self):      #TO DISPLAY THE STRING PROVIDED INSTEAD OF THE OBJECT
        return f"{self.borrower} borrowed {self.borrowed_book}"
from django.db import models
from uuid import uuid4

class MyUser(models.Model):
    
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
    
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=6, choices=Gender.choices)
    img = models.ImageField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    email_token = models.UUIDField(default=uuid4, unique=True, editable=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creation_date']

    
    def __str__(self):
        return self.username
    
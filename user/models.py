from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Film(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User, related_name='films')

    def __str__(self):
        return self.name



STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)
class Employee(models.Model):
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=128, default='Active', choices=STATUS)

    def __str__(self):
        return self.name

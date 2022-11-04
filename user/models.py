from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

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





class Movie(models.Model):

    title = models.CharField(max_length=40, unique=True)

    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1895),
            MaxValueValidator(2050),
        ]
    )

    rating = models.PositiveSmallIntegerField(choices=(
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


MARRIED_STATUS = (
    ('Married', 'Married'),
    ('Single', 'Single'),
)

class Married(models.Model):
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=128, default='Married', choices=MARRIED_STATUS)
    wife = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name
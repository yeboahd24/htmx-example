from django.contrib import admin
from .models import Film, Employee, User, Married

# Register your models here.
admin.site.register(Film)
admin.site.register(Employee)
admin.site.register(User)
admin.site.register(Married)


from django.contrib.auth.forms import UserCreationForm
from user.models import User, Employee
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name"]

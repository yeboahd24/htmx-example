from django.contrib.auth.forms import UserCreationForm
from user.models import User, Employee, Married
from django import forms
from django.forms import fields, widgets


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name"]


class MarriedForm(forms.ModelForm):
    class Meta:
        model = Married
        fields = ["name", "status", "wife"]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'name': 'name', 'id': 'name', 'placeholder': 'Enter name'}),
            'status': forms.Select(attrs={'class': 'form-control', 'name': 'status', 'id': 'status'}),
            'wife': forms.HiddenInput(attrs={'class': 'form-control', 'name': 'wife', 'id': 'wife'}),
        }

   
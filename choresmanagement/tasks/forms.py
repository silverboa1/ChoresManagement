from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name", "description", "category", "difficulty", 
            "expected_time", "periodicity", "priority", "status"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "difficulty": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "expected_time": forms.TextInput(attrs={"class": "form-control", "placeholder": "год:хв:сек"}),
            "periodicity": 
forms.Select
(attrs={"class": "form-select"}),
            "priority": 
forms.Select
(attrs={"class": "form-select"}),
            "status": 
forms.Select
(attrs={"class": "form-select"}),
        }
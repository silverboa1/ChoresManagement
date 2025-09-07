from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory, ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'discription', 'priority', 'status', 'due_date', 'progress')

        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва завдання'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опис завдання', "rows": 4}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', "min": 0, "max": 100})
        }
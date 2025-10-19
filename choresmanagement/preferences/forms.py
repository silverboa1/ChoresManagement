from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from .models import (
    UserPreference,
    UserCategoryPreference,
    UserCategoryExperience,
    UserPhysicalLimitation,
    PhysicalLimitation
)
from tasks.models import TaskCategory

User = get_user_model()


# --- Основна форма користувацьких налаштувань ---
class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['available_time_per_day', 'available_time_per_week']
        widgets = {
            'available_time_per_day': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'available_time_per_week': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


# --- Категорії переваг ---
class UserCategoryPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserCategoryPreference
        fields = ['category', 'preference']
        widgets = {
            'category': 
forms.Select
(attrs={'class': 'form-select'}),
            'preference': 
forms.Select
(attrs={'class': 'form-select'}),
        }


UserCategoryPreferenceFormSet = inlineformset_factory(
    parent_model=User,
    model=UserCategoryPreference,
    form=UserCategoryPreferenceForm,
    extra=1,
    can_delete=True
)


# --- Категорії досвіду ---
class UserCategoryExperienceForm(forms.ModelForm):
    class Meta:
        model = UserCategoryExperience
        fields = ['category', 'experience_level']
        widgets = {
            'category': 
forms.Select
(attrs={'class': 'form-select'}),
            'experience_level': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
        }


UserCategoryExperienceFormSet = inlineformset_factory(
    parent_model=User,
    model=UserCategoryExperience,
    form=UserCategoryExperienceForm,
    extra=1,
    can_delete=True
)


# --- Фізичні обмеження ---

class PhysicalLimitationForm(forms.ModelForm):
    class Meta:
        model = PhysicalLimitation
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserPhysicalLimitationForm(forms.ModelForm):
    class Meta:
        model = UserPhysicalLimitation
        fields = ['limitation']
        widgets = {
            'limitation': 
forms.Select
(attrs={'class': 'form-select'}),
        }


UserPhysicalLimitationFormSet = inlineformset_factory(
    parent_model=User,
    model=UserPhysicalLimitation,
    form=UserPhysicalLimitationForm,
    extra=1,
    can_delete=True
)
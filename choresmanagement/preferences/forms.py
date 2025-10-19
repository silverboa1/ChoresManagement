from django import forms
from django.forms import inlineformset_factory
from django.conf import settings
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

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['available_time_per_day', 'available_time_per_week']
        widgets = {
            'available_time_per_day': forms.TimeInput(attrs={'type': 'time'}),
            'available_time_per_week': forms.TimeInput(attrs={'type': 'time'}),
        }

class UserCategoryPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserCategoryPreference
        fields = ['category', 'preference']
        widgets = {
            'category': 
forms.Select
(),
            'preference': 
forms.Select
()
        }

UserCategoryPreferenceFormSet = inlineformset_factory(
    parent_model=User,
    model=UserCategoryPreference,
    form=UserCategoryPreferenceForm,
    extra=1,  
    can_delete=True
)

class UserCategoryExperienceForm(forms.ModelForm):
    class Meta:
        model = UserCategoryExperience
        fields = ['category', 'experience_level']
        widgets = {
            'category': 
forms.Select
(),
            'experience_level': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }

UserCategoryExperienceFormSet = inlineformset_factory(
    parent_model=User,
    model=UserCategoryExperience,
    form=UserCategoryExperienceForm,
    extra=1,
    can_delete=True
)

class UserPhysicalLimitationForm(forms.ModelForm):
    class Meta:
        model = UserPhysicalLimitation
        fields = ['limitation']
        widgets = {
            'limitation': 
forms.Select
()
        }

UserPhysicalLimitationFormSet = inlineformset_factory(
    parent_model=User,
    model=UserPhysicalLimitation,
    form=UserPhysicalLimitationForm,
    extra=1,
    can_delete=True
)
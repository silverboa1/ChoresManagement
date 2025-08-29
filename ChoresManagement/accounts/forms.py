from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import User, UserProfile, UserPreferences, UserAvailability


class UserRegistrationForm(UserCreationForm):
    """Форма реєстрації користувача"""
    
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email')
        })
    )
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your first name')
        })
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your last name')
        })
    )
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Choose a username')
        })
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter password')
        })
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm password')
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('User with this email already exists'))
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('User with this username already exists'))
        return username


class UserLoginForm(forms.Form):
    """Форма авторизації користувача"""
    
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email'),
            'autofocus': True
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password')
        })
    )
    remember_me = forms.BooleanField(
        label=_('Remember me'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Форма редагування профілю користувача"""
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'timezone', 'language', 
            'experience_level', 'preferred_task_time'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Tell about yourself...')
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('City, Country')
            }),
            'timezone': forms.Select(attrs={
                'class': 'form-select'
            }),
            'language': forms.Select(attrs={
                'class': 'form-select'
            }),
            'experience_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'preferred_task_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 5,
                'max': 480
            }),
        }
        labels = {
            'bio': _('About me'),
            'location': _('Location'),
            'timezone': _('Timezone'),
            'language': _('Language'),
            'experience_level': _('Experience level (1-5)'),
            'preferred_task_time': _('Preferred task duration (minutes)'),
        }


class UserPreferencesForm(forms.ModelForm):
    """Форма редагування переваг користувача"""
    
    class Meta:
        model = UserPreferences
        fields = [
            'preferred_difficulty', 'auto_assign_tasks', 'max_daily_tasks',
            'max_weekly_hours', 'reminder_before_hours', 'allow_weekend_tasks'
        ]
        widgets = {
            'preferred_difficulty': forms.Select(attrs={
                'class': 'form-select'
            }),
            'auto_assign_tasks': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'max_daily_tasks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20
            }),
            'max_weekly_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 50
            }),
            'reminder_before_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 72
            }),
            'allow_weekend_tasks': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'preferred_difficulty': _('Preferred difficulty'),
            'auto_assign_tasks': _('Allow automatic task assignment'),
            'max_daily_tasks': _('Maximum daily tasks'),
            'max_weekly_hours': _('Maximum weekly hours'),
            'reminder_before_hours': _('Remind me (hours before)'),
            'allow_weekend_tasks': _('Allow weekend tasks'),
        }


class UserAvailabilityForm(forms.ModelForm):
    """Форма для одного слота доступності"""
    
    class Meta:
        model = UserAvailability
        fields = ['weekday', 'start_time', 'end_time', 'is_available']
        widgets = {
            'weekday': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'weekday': _('Day of week'),
            'start_time': _('Start time'),
            'end_time': _('End time'),
            'is_available': _('Available'),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError(_('Start time must be before end time'))
        
        return cleaned_data


# Formset для управління множинними слотами доступності
UserAvailabilityFormSet = inlineformset_factory(
    User,
    UserAvailability,
    form=UserAvailabilityForm,
    extra=1,
    can_delete=True,
    fk_name='user'
)


class UserSearchForm(forms.Form):
    """Форма пошуку користувачів"""
    
    query = forms.CharField(
        label=_('Search'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search by name, username, or email...'),
            'autocomplete': 'off'
        })
    )
    
    experience_level = forms.ChoiceField(
        label=_('Experience level'),
        choices=[('', _('Any'))] + [(i, i) for i in range(1, 6)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    language = forms.ChoiceField(
        label=_('Language'),
        choices=[('', _('Any'))] + UserProfile.LANGUAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    is_available_now = forms.BooleanField(
        label=_('Available now'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class BulkUserActionForm(forms.Form):
    """Форма для масових дій з користувачами (для адміністрування)"""
    
    ACTION_CHOICES = [
        ('', _('Select action')),
        ('activate', _('Activate users')),
        ('deactivate', _('Deactivate users')),
        ('send_notification', _('Send notification')),
        ('export_data', _('Export user data')),
    ]
    
    action = forms.ChoiceField(
        label=_('Action'),
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    user_ids = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    message = forms.CharField(
        label=_('Message'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Optional message for notification...')
        })
    )
    
    def clean_user_ids(self):
        user_ids = self.cleaned_data.get('user_ids')
        if not user_ids:
            raise ValidationError()
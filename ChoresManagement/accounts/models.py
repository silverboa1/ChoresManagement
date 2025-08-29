from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Розширена модель користувача"""
    
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', null=True, blank=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'accounts_user'
    
    def str(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class UserProfile(models.Model):
    """Додаткова інформація профілю користувача"""
    
    TIMEZONE_CHOICES = [
        ('Europe/Kiev', _('Kyiv')),
        ('Europe/London', _('London')),
        ('America/New_York', _('New York')),
        ('America/Los_Angeles', _('Los Angeles')),
        ('Asia/Tokyo', _('Tokyo')),
    ]
    
    LANGUAGE_CHOICES = [
        ('uk', _('Ukrainian')),
        ('en', _('English')),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name=_('user')
    )
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    timezone = models.CharField(
        _('timezone'), 
        max_length=50, 
        choices=TIMEZONE_CHOICES, 
        default='Europe/Kiev'
    )
    language = models.CharField(
        _('language'), 
        max_length=5, 
        choices=LANGUAGE_CHOICES, 
        default='uk'
    )
    
    # Додаткові поля для домашніх справ
    experience_level = models.PositiveSmallIntegerField(
        _('experience level'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text=_('1 - beginner, 5 - expert')
    )
    preferred_task_time = models.PositiveSmallIntegerField(
        _('preferred task duration (minutes)'),
        validators=[MinValueValidator(5), MaxValueValidator(480)],
        default=30
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        db_table = 'accounts_userprofile'
    
    def str(self):
        return f"Profile of {self.user.full_name or self.user.username}"

class UserPreferences(models.Model):
    """Особисті переваги користувача щодо завдань"""
    
    DIFFICULTY_CHOICES = [
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='preferences',
        verbose_name=_('user')
    )
    
    # Переваги щодо типів завдань
    preferred_categories = models.JSONField(
        _('preferred task categories'),
        default=list,
        blank=True,
        help_text=_('List of preferred task category IDs')
    )
    avoided_categories = models.JSONField(
        _('avoided task categories'),
        default=list,
        blank=True,
        help_text=_('List of avoided task category IDs')
    )
    
    # Переваги щодо складності
    preferred_difficulty = models.CharField(
        _('preferred difficulty'),
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    
    # Налаштування автоматичного розподілу
    auto_assign_tasks = models.BooleanField(
        _('auto assign tasks'),
        default=True,
        help_text=_('Allow automatic task assignment')
    )
    max_daily_tasks = models.PositiveSmallIntegerField(
        _('maximum daily tasks'),
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        default=3
    )
    max_weekly_hours = models.PositiveSmallIntegerField(
        _('maximum weekly hours'),
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        default=10
    )
    
    # Переваги щодо нагадувань
    reminder_before_hours = models.PositiveSmallIntegerField(
        _('reminder before hours'),
        validators=[MinValueValidator(1), MaxValueValidator(72)],
        default=2
    )
    allow_weekend_tasks = models.BooleanField(
        _('allow weekend tasks'),
        default=True
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('User Preferences')
        verbose_name_plural = _('User Preferences')
        db_table = 'accounts_userpreferences'
    
    def str(self):
        return f"Preferences of {self.user.full_name or self.user.username}"

class UserAvailability(models.Model):
    """Часова доступність користувача"""
    
    WEEKDAY_CHOICES = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='availability_schedule',
        verbose_name=_('user')
    )
    weekday = models.PositiveSmallIntegerField(
        _('weekday'),
        choices=WEEKDAY_CHOICES
    )
    start_time = models.TimeField(_('start time'))
    end_time = models.TimeField(_('end time'))
    is_available = models.BooleanField(_('is available'), default=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('User Availability')
        verbose_name_plural = _('User Availability')
        db_table = 'accounts_useravailability'
        unique_together = ['user', 'weekday', 'start_time']
        ordering = ['weekday', 'start_time']
    
    def str(self):
        weekday_name = dict(self.WEEKDAY_CHOICES)[self.weekday]
        return f"{self.user.username} - {weekday_name} {self.start_time}-{self.end_time}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_time >= self.end_time:
            raise ValidationError(_('Start time must be before end time'))
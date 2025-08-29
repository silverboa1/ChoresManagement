from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    CreateView, UpdateView, DetailView, FormView, 
    TemplateView, View
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User, UserProfile, UserPreferences, UserAvailability
from .forms import (
    UserRegistrationForm, 
    UserLoginForm, 
    UserProfileForm, 
    UserPreferencesForm,
    UserAvailabilityFormSet
)


class RegisterView(CreateView):
    """Реєстрація нового користувача"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile_setup')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                # Автентифікація після реєстрації
                user = authenticate(
                    username=self.object.email,
                    password=form.cleaned_data['password1']
                )
                if user:
                    login(self.request, user)
                    messages.success(self.request, _('Registration successful! Welcome!'))
                return response
        except Exception as e:
            messages.error(self.request, _('Registration error. Please try again.'))
            return self.form_invalid(form)


class LoginView(FormView):
    """Авторизація користувача"""
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        
        if user:
            login(self.request, user)
            messages.success(self.request, _('Login successful!'))
            
            # Перевірка remember_me
            if not form.cleaned_data.get('remember_me'):
                self.request.session.set_expiry(0)  # закрити сесію при закритті браузера
            
            # Редірект на наступну сторінку або дашборд
            next_url = self.request.GET.get('next', self.success_url)
            return redirect(next_url)
        else:
            messages.error(self.request, _('Invalid email or password'))
            return self.form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    """Вихід користувача"""
    
    def post(self, request):
        logout(request)
        messages.success(request, _('You have been logged out successfully'))
        return redirect('accounts:login')
    
    def get(self, request):
        return self.post(request)

class ProfileView(LoginRequiredMixin, DetailView):
    """Перегляд профілю користувача"""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context.update({
            'profile': user.profile,
            'preferences': user.preferences,
            'availability': UserAvailability.objects.filter(
                user=user
            ).order_by('weekday', 'start_time'),
        })
        return context


class ProfileSetupView(LoginRequiredMixin, TemplateView):
    """Початкове налаштування профілю після реєстрації"""
    template_name = 'accounts/profile_setup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_form': UserProfileForm(instance=self.request.user.profile),
            'preferences_form': UserPreferencesForm(instance=self.request.user.preferences),
            'is_setup': True,
        })
        return context
    
    def post(self, request, *args, **kwargs):
        profile_form = UserProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        preferences_form = UserPreferencesForm(
            request.POST, 
            instance=request.user.preferences
        )
        
        if profile_form.is_valid() and preferences_form.is_valid():
            profile_form.save()
            preferences_form.save()
            messages.success(request, _('Profile setup completed!'))
            return redirect('dashboard')
        
        # Якщо форми невалідні, повертаємо з помилками
        context = self.get_context_data()
        context.update({
            'profile_form': profile_form,
            'preferences_form': preferences_form,
        })
        return render(request, self.template_name, context)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Редагування профілю користувача"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully!'))
        return super().form_valid(form)

class PreferencesEditView(LoginRequiredMixin, UpdateView):
    """Редагування переваг користувача"""
    model = UserPreferences
    form_class = UserPreferencesForm
    template_name = 'accounts/preferences_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user.preferences
    
    def form_valid(self, form):
        messages.success(self.request, _('Preferences updated successfully!'))
        return super().form_valid(form)


class AvailabilityEditView(LoginRequiredMixin, TemplateView):
    """Редагування часової доступності"""
    template_name = 'accounts/availability_edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = UserAvailabilityFormSet(
            queryset=UserAvailability.objects.filter(user=self.request.user)
        )
        return context
    
    def post(self, request, *args, **kwargs):
        formset = UserAvailabilityFormSet(
            request.POST, 
            queryset=UserAvailability.objects.filter(user=request.user)
        )
        
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            
            # Видалення позначених для видалення
            for obj in formset.deleted_objects:
                obj.delete()
            
            messages.success(request, _('Availability updated successfully!'))
            return redirect('accounts:profile')
        
        context = self.get_context_data()
        context['formset'] = formset
        return render(request, self.template_name, context)

class ChangePasswordView(LoginRequiredMixin, FormView):
    """Зміна пароля користувача"""
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Важливо для збереження сесії
        messages.success(self.request, _('Password changed successfully!'))
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, View):
    """Видалення облікового запису користувача"""
    
    def post(self, request):
        password = request.POST.get('password')
        
        if not password:
            messages.error(request, _('Password is required'))
            return redirect('accounts:profile')
        
        if not request.user.check_password(password):
            messages.error(request, _('Invalid password'))
            return redirect('accounts:profile')
        
        # Видалення користувача (каскадно видалить всі пов'язані дані)
        username = request.user.username
        request.user.delete()
        messages.success(request, _(f'Account {username} has been deleted'))
        return redirect('accounts:register')
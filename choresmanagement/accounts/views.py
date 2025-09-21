from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth import get_user_model
from .models import Family
from .forms import FamilyForm, CustomLoginForm
from .mixins import FamilyMixin, RoleRequiredMixin

User = get_user_model()

# -----------------------------
# CRUD для Family
# -----------------------------

class FamilyListView(RoleRequiredMixin, ListView):
    model = Family
    template_name = "accounts/family_list.html"
    context_object_name = "families"
    required_roles = ["parent"]  # тільки батьки можуть переглядати список сімей


class FamilyDetailView(RoleRequiredMixin, DetailView):
    model = Family
    template_name = "accounts/family_detail.html"
    context_object_name = "family"
    required_roles = ["parent"]


class FamilyCreateView(RoleRequiredMixin, CreateView):
    model = Family
    form_class = FamilyForm
    template_name = "accounts/family_form.html"
    success_url = reverse_lazy("accounts:family_list")
    required_roles = ["parent"]


class FamilyUpdateView(RoleRequiredMixin, UpdateView):
    model = Family
    form_class = FamilyForm
    template_name = "accounts/family_form.html"
    success_url = reverse_lazy("accounts:family_list")
    required_roles = ["parent"]


class FamilyDeleteView(RoleRequiredMixin, DeleteView):
    model = Family
    template_name = "accounts/family_confirm_delete.html"
    success_url = reverse_lazy("accounts:family_list")
    required_roles = ["parent"]


from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# -----------------------------
# Login / Logout
# -----------------------------

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True  # якщо вже авторизований, відправляти на home
    extra_context = {"title": "Вхід"}

    def get_success_url(self):
        # після входу можна направляти на список сімей або на домашню сторінку
        return reverse_lazy("accounts:family_list")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")  # після виходу повертаємо на сторінку входу
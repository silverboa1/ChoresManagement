from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Family


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Відображення списку користувачів
    list_display = ("username", "email", "role", "family", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "family__name")
    ordering = ("username",)

    # Поля у формі додавання / редагування
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Особисті дані", {"fields": ("first_name", "last_name", "email")}),
        ("Сім'я та роль", {"fields": ("role", "family")}),
        ("Права доступу", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Дати", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "family", "password1", "password2", "is_active", "is_staff"),
        }),
    )
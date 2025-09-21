from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Family, User


class FamilyMixin(LoginRequiredMixin):
    """
    Обмежує доступ до об'єктів лише в межах сім'ї користувача
    """
    family_field = "family"  # ім'я ForeignKey до Family

    def get_queryset(self):
        qs = super().get_queryset()
        family = self.request.user.family
        if family:
            return qs.filter(**{self.family_field: family})
        return qs.none()


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Дозволяє доступ тільки користувачам з певною роллю
    Використання: class MyView(RoleRequiredMixin, View): required_roles = ['parent']
    """
    required_roles: list[str] = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.required_roles and request.user.role not in self.required_roles:
            raise PermissionDenied("Недостатньо прав для доступу")
        return super().dispatch(request, *args, **kwargs)


class OwnerOrParentRequiredMixin(LoginRequiredMixin):
    """
    Доступ дозволено власнику об'єкта або батькам у сім'ї
    """
    model = None  # потрібно вказати у View

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs.get("pk"))

        # власник
        if obj == request.user:
            return super().dispatch(request, *args, **kwargs)

        # батько/мати з тієї ж сім'ї
        if (
            request.user.role == User.PARENT
            and obj.family == request.user.family
        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Недостатньо прав для доступу")

class OwnerOrParentRequiredMixin(LoginRequiredMixin):
    """
    Доступ дозволено власнику об'єкта або батькам у сім'ї
    """
    model = None  # потрібно вказати у View

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs.get("pk"))

        # власник
        if obj == request.user:
            return super().dispatch(request, *args, **kwargs)

        # батько/мати з тієї ж сім'ї
        if (
            request.user.role == User.PARENT
            and 
obj.family
 == 
request.user.family

        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Недостатньо прав для доступу")
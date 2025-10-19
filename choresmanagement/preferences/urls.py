from django.urls import path
from .views import (
    edit_preferences,
    PhysicalLimitationListView,
    PhysicalLimitationDetailView,
    PhysicalLimitationCreateView,
    PhysicalLimitationUpdateView,
    PhysicalLimitationDeleteView,
)

app_name = "preferences"

urlpatterns = [
    path("edit/", edit_preferences, name="edit"),

    path("limitations/", PhysicalLimitationListView.as_view(), name="limitation_list"),
    path("limitations/create/", PhysicalLimitationCreateView.as_view(), name="limitation_create"),
    path("limitations/<int:pk>/", PhysicalLimitationDetailView.as_view(), name="limitation_detail"),
    path("limitations/<int:pk>/update/", PhysicalLimitationUpdateView.as_view(), name="limitation_update"),
    path("limitations/<int:pk>/delete/", PhysicalLimitationDeleteView.as_view(), name="limitation_delete"),
]
from django.db import models
from django.conf import settings
from tasks.models import TaskCategory

# Create your models here.
class UserPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences"
    )

    # доступний час (наприклад, у хвилинах на день або тиждень)
    available_time_per_day = models.DurationField(
        null=True, blank=True, verbose_name="Доступний час на день"
    )
    available_time_per_week = models.DurationField(
        null=True, blank=True, verbose_name="Доступний час на тиждень"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Налаштування користувача"
        verbose_name_plural = "Налаштування користувачів"

    def __str__(self):
        return f"Налаштування для {self.user.username}"


class UserCategoryPreference(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    PREFERENCE_CHOICES = [
        (LIKE, "Улюблена"),
        (DISLIKE, "Неулюблена"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="category_preferences"
    )
    category = models.ForeignKey(
        TaskCategory, on_delete=models.CASCADE, related_name="user_preferences"
    )
    preference = models.CharField(
        max_length=10, choices=PREFERENCE_CHOICES, verbose_name="Вподобання"
    )

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.username}: {self.get_preference_display()} {
self.category.name
}"


class UserCategoryExperience(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="category_experience"
    )
    category = models.ForeignKey(
        TaskCategory, on_delete=models.CASCADE, related_name="user_experience"
    )
    experience_level = models.PositiveSmallIntegerField(
        default=1, verbose_name="Рівень досвіду (1-5)"
    )

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.username} - {
self.category.name
}: {self.experience_level}"

class PhysicalLimitation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва обмеження")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.name



class UserPhysicalLimitation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="physical_limitations"
    )
    limitation = models.ForeignKey(
        PhysicalLimitation, on_delete=models.CASCADE, related_name="users"
    )

    class Meta:
        unique_together = ("user", "limitation")

    def __str__(self):
        return f"{self.user.username} - {
self.limitation.name
}"
from django.db import models

class Task(models.Model):
    PERIOD_CHOICES = [
        ("once", "Одноразове"),
        ("daily", "Щоденне"),
        ("weekly", "Щотижневе"),
        ("monthly", "Щомісячне"),
    ]

    PRIORITY_CHOICES = [
        (1, "Низький"),
        (2, "Середній"),
        (3, "Високий"),
    ]

    STATUS_CHOICES = [
        ("planned", "Заплановано"),
        ("in_progress", "В роботі"),
        ("completed", "Виконано"),
        ("canceled", "Відмінено"),
    ]

    name = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="planned",verbose_name="Статус")
    category = models.CharField(max_length=100, verbose_name="Категорія")
    difficulty = models.PositiveSmallIntegerField(default=1, verbose_name="Складність (1-5)")
    expected_time = models.DurationField(verbose_name="Очікуваний час виконання")
    periodicity = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="once", verbose_name="Періодичність")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="Пріоритет")
    is_archived = models.BooleanField(default=False, verbose_name="Архівоване")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"

    def __str__(self):
        return self.name
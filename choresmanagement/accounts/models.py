from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, verbose_name="Опис") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    PARENT = 'parent'
    CHILD = 'child'
    ROLE_CHOICES = [
        (PARENT, 'Батько/Мати'),
        (CHILD, 'Дитина'),
    ]


    family = models.ForeignKey(
        Family, on_delete=models.SET_NULL, null=True, blank=True, related_name='members'
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CHILD)
    birth_date = models.DateField(null=True, blank=True)
from django.contrib.auth.models import AbstractUser
from django.db import models

class Employee(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    hired_at = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name} [{self.username}]"
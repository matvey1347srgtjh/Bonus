from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class Employee(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    department = models.CharField(max_length=255, blank=True, verbose_name="Отдел")
    position = models.CharField(max_length=255, blank=True, verbose_name="Должность")
    hired_at = models.DateField(null=True, blank=True, verbose_name="Дата приема")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    
    needs_password_change = models.BooleanField(
        default=True, 
        verbose_name="Требуется смена пароля"
    )
    
    mentor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='interns',
        verbose_name="Ментор",
    )
    is_intern = models.BooleanField(default=False, verbose_name="Стажёр")
    trial_passed = models.BooleanField(default=False, verbose_name="Стажировка пройдена")
    profile_bonus_received = models.BooleanField(default=False, verbose_name="Бонус за заполнение профиля получен")
    
    def clean(self):
        super().clean()
        if self.mentor:
            if not self.is_intern:
                raise ValidationError("Ментора можно назначить только стажеру.")
            if self.pk and self.mentor_id == self.pk:
                raise ValidationError("Нельзя быть ментором самому себе.")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.username})"
        
class CheckIn(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='check_ins', verbose_name="Сотрудник")
    timestamp = models.DateTimeField("Время прохода")
    is_entry = models.BooleanField("Вход", default=True)

    class Meta:
        verbose_name = "Проход через проходную"
        verbose_name_plural = "Логи проходной"

    def __str__(self):
        direction = "Вход" if self.is_entry else "Выход"
        return f"{self.employee.last_name} {self.employee.first_name} | {direction} | {self.timestamp.strftime('%d.%m.%Y %H:%M')}"
    
class WorkPlan(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="Сотрудник")
    month = models.DateField("Месяц плана", help_text="Первое число месяца")
    target_tasks = models.PositiveIntegerField("Цель (кол-во задач/деталей)")
    completed_tasks = models.PositiveIntegerField("Выполнено", default=0)
    is_rewarded = models.BooleanField("Бонус начислен", default=False)

    class Meta:
        verbose_name = "План работ"
        verbose_name_plural = "Планы работ"
        unique_together = ('employee', 'month')

    def __str__(self):
        return f"План {self.employee.last_name} за {self.month.strftime('%m.%Y')}"
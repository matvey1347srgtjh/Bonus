from django.db import models

class RewardSetting(models.Model):
    title = models.CharField("Название заслуги", max_length=255)
    code = models.SlugField("Технический код", unique=True, help_text="Например: 'birthday' или 'punctuality'")
    amount = models.PositiveIntegerField("Сумма вознаграждения", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        verbose_name = "Настройка вознаграждения"
        verbose_name_plural = "Настройки вознаграждений"

    def __str__(self):
        return f"{self.title}: {self.amount} Баллов"
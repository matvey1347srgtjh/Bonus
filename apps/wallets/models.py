from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.balance}"
    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Начисление'),
        ('OUT', 'Списание'),
        ('REF', 'Возврат'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name="Кошелек")
    amount = models.PositiveIntegerField(verbose_name="Сумма")
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES, verbose_name="Тип")
    reason = models.CharField(max_length=255, verbose_name="Причина")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
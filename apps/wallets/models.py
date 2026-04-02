from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.balance}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Начисление'),
        ('OUT', 'Списание'),
        ('REF', 'Возврат'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
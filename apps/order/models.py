import uuid
from django.db import models
from django.conf import settings
from apps.merch.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('READY', 'Готов к выдаче'),
        ('DONE', 'Выдан'),
        ('CANCELED', 'Отменен'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NEW')
    total_price = models.PositiveIntegerField()
    qr_code_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.PositiveIntegerField()
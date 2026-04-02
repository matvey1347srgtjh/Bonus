from django.db import models

class RewardRule(models.Model):
    name = models.CharField(max_length=255)
    reward_amount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.reward_amount})"
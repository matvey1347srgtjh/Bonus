from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from apps.wallets.models import Wallet

@receiver(post_save, sender=Employee)
def create_employee_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.get_or_create(user=instance)

@receiver(post_save, sender=Employee)
def check_profile_completion(sender, instance, **kwargs):
    if not instance.profile_bonus_received:
        required_fields = [
            instance.first_name, 
            instance.last_name, 
            instance.middle_name, 
            instance.phone, 
            instance.position,
            instance.department
        ]
        
        if all(required_fields):
            from apps.wallets.services import WalletService
            WalletService.add_coins(
                employee=instance,
                amount=300,
                reason="Цифровой след: Полное заполнение профиля"
            )
            instance.profile_bonus_received = True
            instance.save(update_fields=['profile_bonus_received'])
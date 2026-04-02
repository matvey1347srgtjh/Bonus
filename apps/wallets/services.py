from django.db import transaction
from .models import Wallet, Transaction

class WalletService:
    @staticmethod
    def add_coins(employee, amount, reason):
        with transaction.atomic():
            wallet, created = Wallet.objects.get_or_create(user=employee)
            wallet.balance += amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                type='IN',
                reason=reason
            )
        return wallet

class RewardService:
    @staticmethod
    def approve_trial_period(intern):
        if intern.is_intern and not intern.trial_passed:
            intern.trial_passed = True
            intern.save()
            
            if intern.mentor:
                from .services import WalletService
                WalletService.add_coins(
                    employee=intern.mentor,
                    amount=2000,
                    reason=f"Наставничество: Стажер {intern.username} прошел срок"
                )
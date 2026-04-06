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

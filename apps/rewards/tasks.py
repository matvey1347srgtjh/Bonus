from celery import shared_task
from django.utils import timezone
from apps.users.models import Employee
from apps.wallets.services import WalletService

@shared_task
def check_birthdays_and_award():
    today = timezone.now().date()
    birthday_boys = Employee.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )
    
    for employee in birthday_boys:
        WalletService.add_coins(
            employee=employee,
            amount=1000,
            reason="Подарок на день рождения от АО ИРЗ"
        )

@shared_task
def check_work_anniversary_award():
    today = timezone.now().date()
    veterans = Employee.objects.filter(
        hired_at__month=today.month,
        hired_at__day=today.day
    ).exclude(hired_at__year=today.year)
    
    for employee in veterans:
        years = today.year - employee.hired_at.year
        amount = 500 * years
        WalletService.add_coins(
            employee=employee,
            amount=amount,
            reason=f"Бонус за выслугу лет ({years} лет в АО ИРЗ)"
        )
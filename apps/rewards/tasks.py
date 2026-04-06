from celery import shared_task
from django.utils import timezone
from django.db import models
from datetime import timedelta
from apps.users.models import Employee, CheckIn, WorkPlan
from apps.wallets.services import WalletService
from .services import RewardService
from apps.wallets.models import Transaction, Wallet

@shared_task
def check_birthdays_and_award():
    from apps.wallets.models import Transaction
    today = timezone.now().date()
    
    birthday_boys = Employee.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )
    
    reward_amount = RewardService.get_reward_amount('birthday')
    
    if reward_amount > 0:
        for employee in birthday_boys:
            already_rewarded = Transaction.objects.filter(
                wallet__user=employee,
                reason__icontains="день рождения",
                created_at__year=today.year
            ).exists()
            
            if not already_rewarded:
                WalletService.add_coins(
                    employee=employee,
                    amount=reward_amount,
                    reason=f"Подарок на день рождения от АО ИРЗ ({today.year})"
                )

@shared_task
def check_work_anniversary_award():
    today = timezone.now().date()
    
    amount_1 = RewardService.get_reward_amount('anniversary_1')
    amount_5 = RewardService.get_reward_amount('anniversary_5')
    amount_10 = RewardService.get_reward_amount('anniversary_10')

    veterans = Employee.objects.filter(
        hired_at__month=today.month,
        hired_at__day=today.day
    ).exclude(hired_at__year=today.year)
    
    for employee in veterans:
        years = today.year - employee.hired_at.year
        
        already_rewarded = Transaction.objects.filter(
        wallet__user=employee,
        reason__icontains=f"выслугу лет ({years}", 
        created_at__year=today.year
        ).exists()

        if not already_rewarded:
            if years >= 10:
                amount = amount_10
            elif years >= 5:
                amount = amount_5
            else:
                amount = amount_1
                
            if amount > 0:
                WalletService.add_coins(
                    employee=employee,
                    amount=amount,
                    reason=f"Бонус за выслугу лет ({years} лет в АО ИРЗ)"
                )
            
@shared_task
def reward_perfect_attendance():
    now = timezone.now()
    first_day_current = now.replace(day=1)
    last_day_prev = first_day_current - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    
    reward_amount = RewardService.get_reward_amount('punctuality')
    
    if reward_amount <= 0:
        return

    employees = Employee.objects.all()
    
    for emp in employees:
        lates = CheckIn.objects.filter(
            employee=emp,
            timestamp__date__range=[first_day_prev, last_day_prev],
            timestamp__time__gt="08:00:00",
            is_entry=True
        ).exists()

        if not lates:
            has_worked = CheckIn.objects.filter(
                employee=emp,
                timestamp__date__range=[first_day_prev, last_day_prev]
            ).exists()

            if has_worked:
                WalletService.add_coins(
                    employee=emp,
                    amount=reward_amount,
                    reason=f"Дисциплина: Ни одного опоздания за {first_day_prev.strftime('%B %Y')}"
                )

@shared_task
def check_production_plans_and_reward():
    today = timezone.now().date()
    reward_amount = RewardService.get_reward_amount('production_plan_reached')
    
    if reward_amount <= 0:
        return

    successful_plans = WorkPlan.objects.filter(
        completed_tasks__gte=models.F('target_tasks'),
        is_rewarded=False
    )

    for plan in successful_plans:
        WalletService.add_coins(
            employee=plan.employee,
            amount=reward_amount,
            reason=f"Выполнение производственного плана ({plan.month.strftime('%m.%Y')})"
        )
        plan.is_rewarded = True
        plan.save()
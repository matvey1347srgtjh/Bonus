from django.test import TestCase
from django.utils import timezone
from apps.users.models import Employee, WorkPlan, CheckIn
from apps.rewards.models import RewardSetting
from apps.rewards.tasks import (
    check_production_plans_and_reward, 
    check_birthdays_and_award,
    check_work_anniversary_award,
    reward_perfect_attendance
)
from apps.rewards.services import RewardService
from apps.wallets.models import Wallet
import datetime

class FullRewardsTest(TestCase):
    def setUp(self):
        RewardSetting.objects.get_or_create(code='production_plan_reached', defaults={'amount': 750})
        RewardSetting.objects.get_or_create(code='birthday', defaults={'amount': 500})
        RewardSetting.objects.get_or_create(code='anniversary_1', defaults={'amount': 1000})
        RewardSetting.objects.get_or_create(code='mentor_bonus', defaults={'amount': 1500})
        RewardSetting.objects.get_or_create(code='punctuality', defaults={'amount': 300})

        today = timezone.now().date()
        one_year_ago = today.replace(year=today.year - 1)

        self.me = Employee.objects.create(
            username='main_worker',
            date_of_birth=today,
            hired_at=one_year_ago
        )
        self.wallet, _ = Wallet.objects.get_or_create(user=self.me)

    def test_birthday_logic(self):
        """Тест начисления 500 коинов в день рождения"""
        check_birthdays_and_award()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 500)
        print("Тест ДР: Успешно (500 коинов)")

    def test_anniversary_logic(self):
        """Тест начисления 1000 коинов за 1 год стажа"""
        check_work_anniversary_award()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1000)
        print("Тест стажа: Успешно (1000 коинов)")

    def test_production_plan_logic(self):
        """Тест выполнения плана (150 из 150 или выше)"""
        WorkPlan.objects.create(
            employee=self.me,
            month=datetime.date.today().replace(day=1),
            target_tasks=150,
            completed_tasks=150,
            is_rewarded=False
        )
        check_production_plans_and_reward()
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 750)
        print("Тест плана: Успешно (750 коинов)")

    def test_mentor_logic(self):
        """Тест бонуса наставнику за закрытие стажировки"""
        intern = Employee.objects.create(
            username='intern_user', 
            mentor=self.me, 
            is_intern=True
        )
        RewardService.approve_trial_period(intern)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1500)
        print("Тест наставничества: Успешно (1500 коинов)")

def test_attendance_logic(self):
        """Тест бонуса за отсутствие опозданий в прошлом месяце"""
        from django.utils import timezone
        import datetime

        now = timezone.now()
        first_of_this_month = now.replace(day=1)
        last_month_point = first_of_this_month - datetime.timedelta(days=15)
        
        check_time = datetime.datetime.combine(
            last_month_point.date(), 
            datetime.time(7, 45)
        )
        if timezone.is_naive(check_time):
            check_time = timezone.make_aware(check_time)

        CheckIn.objects.create(
            employee=self.me,
            timestamp=check_time,
            is_entry=True
        )
        
        reward_perfect_attendance()
        
        self.wallet.refresh_from_db()
        
        if self.wallet.balance == 0:
            from apps.wallets.models import Transaction
            print("\nТранзакции не найдены. Проверь фильтр даты в tasks.py.")
            print(f"Искали период: {last_month_point.replace(day=1).date()} - {first_of_this_month - datetime.timedelta(days=1)}")

        self.assertEqual(self.wallet.balance, 300)
        print("Тест дисциплины: Успешно (300 коинов)")
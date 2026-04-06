from apps.rewards.models import RewardSetting
from apps.wallets.services import WalletService

class RewardService:
    
    @staticmethod
    def get_reward_amount(code):
        setting = RewardSetting.objects.filter(code=code).first()
        return setting.amount if setting else 0

    @staticmethod
    def approve_trial_period(intern):
        if intern.mentor and not intern.trial_passed:
            intern.trial_passed = True
            intern.is_intern = False
            intern.save()

            reward_amount = RewardService.get_reward_amount('mentor_bonus')

            if reward_amount > 0:
                WalletService.add_coins(
                    employee=intern.mentor,
                    amount=reward_amount, 
                    reason=f"Бонус за наставничество: стажер {intern.get_full_name()}"
                )
            return True
        return False
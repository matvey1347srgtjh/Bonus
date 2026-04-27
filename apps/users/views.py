from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import ProfileUpdateForm
from apps.rewards.models import RewardSetting 

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('merch:index')

    def form_valid(self, form):
        user = form.save()
        user.needs_password_change = False
        user.save()
        
        update_session_auth_hash(self.request, user)
        
        messages.success(self.request, "Пароль успешно изменен! Теперь вам доступен весь функционал системы.")
        return super().form_valid(form)

@login_required
def profile_view(request):
    employee = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            
            if not employee.profile_bonus_received:
                reward_config = RewardSetting.objects.filter(code='profile_complete', is_active=True).first()
                
                if reward_config and hasattr(employee, 'wallet'):
                    employee.wallet.balance += reward_config.amount
                    employee.wallet.save()
                    
                    employee.profile_bonus_received = True
                    employee.save()
                    messages.success(request, f"Профиль заполнен! Вам начислено {reward_config.amount} Баллов.")
                else:
                    employee.profile_bonus_received = True
                    employee.save()
                    messages.warning(request, "Профиль сохранен, но правило начисления 'profile_complete' не найдено.")
            else:
                messages.success(request, "Изменения сохранены.")
                
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=employee)
    
    return render(request, 'users/profile.html', {
        'form': form,
        'employee': employee
    })
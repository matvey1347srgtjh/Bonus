from django.urls import path
from .views import profile_view, CustomPasswordChangeView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    
]
from django.urls import path
from .views import MerchListView

app_name = 'merch'

urlpatterns = [
    path('', MerchListView.as_view(), name='index'),
]
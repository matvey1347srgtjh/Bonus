from django.urls import path
from .views import MerchListView, ProductDetailView, HomeTemplateView

app_name = 'merch'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('shop/', MerchListView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
from django.urls import path
from .views import MerchListView, ProductDetailView

app_name = 'merch'

urlpatterns = [
    path('', MerchListView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
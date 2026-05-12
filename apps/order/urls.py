from django.urls import path
from .views import  cart_add, cart_detail, cart_remove, checkout

app_name = 'orders'

urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
]
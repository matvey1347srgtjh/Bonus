from django.shortcuts import get_object_or_404, redirect, render
from apps.merch.models import Product
from django.db import transaction
from apps.wallets.models import Transaction as WalletTransaction
from .models import Order, OrderItem
from django.contrib import messages

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
        
    request.session['cart'] = cart
    return redirect('merch:index')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total
        })
        
    return render(request, 'order/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    return redirect('orders:cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('merch:index')
        
    user = request.user
    wallet = getattr(user, 'wallet', None)
    
    total_price = 0
    items_to_create = []
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if product.stock < quantity:
            messages.error(request, f'Недостаточно товара {product.name}')
            return redirect('orders:cart_detail')
        total_price += product.price * quantity
        items_to_create.append((product, quantity))

    if wallet.balance < total_price:
        messages.error(request, 'Недостаточно коинов.')
        return redirect('orders:cart_detail')

    try:
        with transaction.atomic():
            wallet.balance -= total_price
            wallet.save()

            WalletTransaction.objects.create(
                wallet=wallet,
                amount=total_price,
                type='OUT',
                reason="Покупка мерча (корзина)"
            )

            order = Order.objects.create(
                user=user,
                total_price=total_price,
                status='NEW'
            )

            for product, quantity in items_to_create:
                product.stock -= quantity
                product.save()
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_purchase=product.price
                )

            request.session['cart'] = {}
            messages.success(request, 'Заказ оформлен!')
            return redirect('users:profile')
            
    except Exception:
        messages.error(request, 'Ошибка при оформлении.')
        return redirect('orders:cart_detail')
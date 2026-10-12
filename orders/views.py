from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderItem
from cart.views import get_or_create_cart


@login_required
def checkout_view(request):
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')
    SHIPPING_FEES = {
        'standard': settings.SHIPPING_STANDARD,
        'express': settings.SHIPPING_EXPRESS,
        'same_day': settings.SHIPPING_SAME_DAY,
    }
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', request.user.email)
        province = request.POST.get('province')
        district = request.POST.get('district')
        ward = request.POST.get('ward')
        street_address = request.POST.get('street_address')
        shipping_method = request.POST.get('shipping_method', 'standard')
        notes = request.POST.get('notes', '')
        shipping_fee = SHIPPING_FEES.get(shipping_method, settings.SHIPPING_STANDARD)
        if cart.subtotal >= settings.FREE_SHIPPING_THRESHOLD:
            shipping_fee = 0
        order = Order(
            user=request.user,
            full_name=full_name, phone=phone, email=email,
            province=province, district=district, ward=ward, street_address=street_address,
            subtotal=cart.subtotal, discount_amount=cart.discount_amount,
            shipping_fee=shipping_fee, total=cart.total + shipping_fee,
            coupon_code=cart.coupon_code, shipping_method=shipping_method, notes=notes,
        )
        order.save()
        order.order_number = f'DH{str(order.id)[:8].upper()}'
        order.save()
        for item in cart.items.all():
            img = item.variant.product.main_image
            OrderItem.objects.create(
                order=order, variant=item.variant,
                product_name=item.variant.product.name,
                color_name=item.variant.color.name if item.variant.color else '',
                size_name=item.variant.size.name if item.variant.size else '',
                unit_price=item.variant.final_price, quantity=item.quantity,
                product_image=img.image.url if img else '',
            )
            item.variant.stock -= item.quantity
            item.variant.save()
            item.variant.product.total_sold += item.quantity
            item.variant.product.save(update_fields=['total_sold'])
        cart.items.all().delete()
        cart.coupon_code = ''
        cart.save()
        return redirect('payment_qr', order_id=order.id)
    addresses = request.user.addresses.all()
    context = {
        'cart': cart, 'addresses': addresses,
        'shipping_fees': SHIPPING_FEES, 'free_threshold': settings.FREE_SHIPPING_THRESHOLD,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = getattr(order, 'payment', None)
    STATUS_STEPS = {
        'pending': 1, 'confirmed': 2, 'processing': 3,
        'shipping': 4, 'delivered': 5, 'cancelled': 0, 'refunded': 0
    }
    steps = [(1, 'Chờ xác nhận'), (2, 'Xác nhận'), (3, 'Đóng gói'), (4, 'Giao hàng'), (5, 'Hoàn thành')]
    order_step = STATUS_STEPS.get(order.status, 0)
    return render(request, 'orders/order_detail.html', {
        'order': order, 'payment': payment,
        'steps': steps, 'order_step': order_step
    })


@login_required
def order_cancel_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Đã hủy đơn hàng {order.order_number}.')
    else:
        messages.error(request, 'Không thể hủy đơn hàng ở trạng thái này.')
    return redirect('order_history')


def order_thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/thank_you.html', {'order': order})

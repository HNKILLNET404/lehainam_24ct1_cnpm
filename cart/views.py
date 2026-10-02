from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import ProductVariant
from django.conf import settings


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('variant__product', 'variant__color', 'variant__size').prefetch_related('variant__product__images')
    free_threshold = settings.FREE_SHIPPING_THRESHOLD
    remaining = max(0, free_threshold - int(cart.subtotal))
    context = {
        'cart': cart, 'items': items,
        'free_threshold': free_threshold, 'remaining_for_free_ship': remaining,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request):
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    variant = get_object_or_404(ProductVariant, id=variant_id)
    if not variant.is_available:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Sản phẩm đã hết hàng'}, status=400)
        messages.error(request, 'Sản phẩm đã hết hàng.')
        return redirect('product_detail', slug=variant.product.slug)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
    if not created:
        item.quantity = min(item.quantity + quantity, variant.stock)
    else:
        item.quantity = min(quantity, variant.stock)
    item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.total_items,
                             'message': f'Đã thêm {variant.product.name} vào giỏ hàng!'})
    messages.success(request, f'Đã thêm {variant.product.name} vào giỏ hàng!')
    return redirect('cart')


@require_POST
def cart_update(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = min(quantity, item.variant.stock)
        item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.total_items, 'cart_total': str(cart.subtotal)})
    return redirect('cart')


@require_POST
def cart_remove(request):
    item_id = request.POST.get('item_id')
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = item.variant.product.name
    item.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.total_items})
    messages.success(request, f'Đã xóa {product_name} khỏi giỏ hàng.')
    return redirect('cart')


@require_POST
def apply_coupon(request):
    from promotions.models import Coupon
    code = request.POST.get('coupon_code', '').strip()
    cart = get_or_create_cart(request)
    try:
        coupon = Coupon.objects.get(code=code, is_active=True)
        if coupon.is_valid():
            cart.coupon_code = code
            cart.save()
            messages.success(request, f'Mã giảm giá "{code}" đã được áp dụng!')
        else:
            messages.error(request, 'Mã giảm giá đã hết hiệu lực.')
    except Coupon.DoesNotExist:
        messages.error(request, 'Mã giảm giá không hợp lệ.')
    return redirect('cart')


def remove_coupon(request):
    cart = get_or_create_cart(request)
    cart.coupon_code = ''
    cart.save()
    messages.info(request, 'Đã xóa mã giảm giá.')
    return redirect('cart')


def mini_cart(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('variant__product').prefetch_related('variant__product__images')
    return render(request, 'cart/mini_cart.html', {'cart': cart, 'items': items})

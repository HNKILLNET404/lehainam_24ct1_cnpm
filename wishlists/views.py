from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Wishlist
from products.models import Product


@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.prefetch_related('images', 'variants').all()
    return render(request, 'wishlists/wishlist.html', {'wishlist': wishlist, 'products': products})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
        messages.info(request, f'Đã xóa {product.name} khỏi danh sách yêu thích.')
    else:
        wishlist.products.add(product)
        added = True
        messages.success(request, f'Đã thêm {product.name} vào danh sách yêu thích!')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'added': added, 'count': wishlist.products.count()})
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

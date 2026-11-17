from django.shortcuts import render
from .models import Coupon, Banner
from django.utils import timezone


def promotions_view(request):
    banners = Banner.objects.filter(is_active=True).order_by('order')
    coupons = Coupon.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now()
    ).filter(
        valid_to__isnull=True
    ) | Coupon.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now()
    )
    return render(request, 'promotions/promotions.html', {
        'banners': banners,
        'coupons': coupons.distinct(),
    })

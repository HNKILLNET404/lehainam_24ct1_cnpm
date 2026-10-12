from django.db import models
from django.conf import settings
from products.models import ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='cart', verbose_name='Khách hàng')
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name='Session key')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_code = models.CharField(max_length=50, blank=True, verbose_name='Mã giảm giá')

    class Meta:
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'

    def __str__(self):
        return f'Cart of {self.user or self.session_key}'

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def discount_amount(self):
        from promotions.models import Coupon
        if self.coupon_code:
            try:
                coupon = Coupon.objects.get(code=self.coupon_code, is_active=True)
                return coupon.calculate_discount(self.subtotal)
            except Coupon.DoesNotExist:
                pass
        return 0

    @property
    def total(self):
        return self.subtotal - self.discount_amount


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Giỏ hàng')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name='Sản phẩm')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sản phẩm trong giỏ'
        verbose_name_plural = 'Sản phẩm trong giỏ'
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f'{self.quantity}x {self.variant}'

    @property
    def total_price(self):
        return self.variant.final_price * self.quantity

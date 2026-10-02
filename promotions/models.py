from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Phần trăm (%)'),
        ('fixed', 'Số tiền cố định'),
    ]
    code = models.CharField(max_length=50, unique=True, verbose_name='Mã giảm giá')
    description = models.CharField(max_length=200, blank=True, verbose_name='Mô tả')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Giá trị giảm')
    minimum_order = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Đơn hàng tối thiểu')
    max_uses = models.IntegerField(default=0, verbose_name='Số lần dùng tối đa (0=không giới hạn)')
    used_count = models.IntegerField(default=0, verbose_name='Số lần đã dùng')
    valid_from = models.DateTimeField(verbose_name='Hiệu lực từ', default=timezone.now)
    valid_to = models.DateTimeField(verbose_name='Hiệu lực đến', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mã giảm giá'
        verbose_name_plural = 'Mã giảm giá'

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False
        return True

    def calculate_discount(self, subtotal):
        if not self.is_valid() or subtotal < self.minimum_order:
            return 0
        if self.discount_type == 'percentage':
            return int(subtotal * self.discount_value / 100)
        return int(min(self.discount_value, subtotal))


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='Phụ đề')
    image = models.ImageField(upload_to='banners/', verbose_name='Ảnh banner')
    image_mobile = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name='Ảnh mobile')
    link = models.CharField(max_length=200, blank=True, verbose_name='Link')
    button_text = models.CharField(max_length=50, blank=True, default='Mua ngay')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banner'
        ordering = ['order']

    def __str__(self):
        return self.title

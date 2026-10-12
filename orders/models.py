from django.db import models
from django.conf import settings
from products.models import ProductVariant
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'), ('confirmed', 'Đã xác nhận'),
        ('processing', 'Đang đóng gói'), ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'), ('cancelled', 'Đã hủy'), ('refunded', 'Đã hoàn tiền'),
    ]
    SHIPPING_METHOD_CHOICES = [
        ('standard', 'Giao tiêu chuẩn (3-5 ngày)'),
        ('express', 'Giao nhanh (1-2 ngày)'),
        ('same_day', 'Giao hỏa tốc (trong ngày)'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, blank=True, verbose_name='Mã đơn hàng')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='orders', verbose_name='Khách hàng')
    full_name = models.CharField(max_length=100, verbose_name='Họ tên')
    phone = models.CharField(max_length=15, verbose_name='Số điện thoại')
    email = models.EmailField(verbose_name='Email')
    province = models.CharField(max_length=100, verbose_name='Tỉnh/Thành phố')
    district = models.CharField(max_length=100, verbose_name='Quận/Huyện')
    ward = models.CharField(max_length=100, verbose_name='Phường/Xã')
    street_address = models.CharField(max_length=255, verbose_name='Địa chỉ')
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Tạm tính')
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Giảm giá')
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Phí ship')
    total = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Tổng cộng')
    coupon_code = models.CharField(max_length=50, blank=True, verbose_name='Mã giảm giá')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHOD_CHOICES, default='standard')
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'DH{str(self.id)[:8].upper()}'
        super().save(*args, **kwargs)

    @property
    def shipping_address(self):
        return f'{self.street_address}, {self.ward}, {self.district}, {self.province}'

    @property
    def status_color(self):
        colors = {
            'pending': 'yellow', 'confirmed': 'blue', 'processing': 'purple',
            'shipping': 'indigo', 'delivered': 'green', 'cancelled': 'red', 'refunded': 'gray'
        }
        return colors.get(self.status, 'gray')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    color_name = models.CharField(max_length=50, blank=True)
    size_name = models.CharField(max_length=20, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField()
    product_image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.quantity}x {self.product_name}'

    @property
    def total_price(self):
        return self.unit_price * self.quantity

from django.db import models
from orders.models import Order
import uuid


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'), ('uploaded', 'Đã upload biện lai'),
        ('confirmed', 'Đã xác nhận'), ('failed', 'Thất bại'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Thanh toán'
        verbose_name_plural = 'Thanh toán'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment for {self.order.order_number}'

from django.db import models
from django.conf import settings
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Số sao')
    title = models.CharField(max_length=100, blank=True, verbose_name='Tiêu đề')
    body = models.TextField(verbose_name='Nội dung')
    is_approved = models.BooleanField(default=True, verbose_name='Hiển thị')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.product.name} ({self.rating}★)'

    @property
    def stars_range(self):
        return range(1, 6)

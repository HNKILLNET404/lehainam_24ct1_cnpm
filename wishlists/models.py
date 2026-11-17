from django.db import models
from django.conf import settings
from products.models import Product


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Danh sách yêu thích'
        verbose_name_plural = 'Danh sách yêu thích'

    def __str__(self):
        return f'Wishlist of {self.user.email}'

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid


class Category(models.Model):
    """Danh mục sản phẩm"""
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Ảnh danh mục")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', verbose_name="Danh mục cha")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """Sản phẩm"""
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('unisex', 'Unisex'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='products', verbose_name="Danh mục")
    description = models.TextField(verbose_name="Mô tả")
    material = models.CharField(max_length=200, blank=True, verbose_name="Chất liệu")
    care_instructions = models.TextField(blank=True, verbose_name="Hướng dẫn bảo quản")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex', verbose_name="Giới tính")
    base_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá gốc (VND)")
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá sale (VND)")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    is_new_arrival = models.BooleanField(default=False, verbose_name="Hàng mới về")
    is_best_seller = models.BooleanField(default=False, verbose_name="Bán chạy")
    total_sold = models.IntegerField(default=0, verbose_name="Tổng đã bán")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        """Giá hiện tại (ưu tiên giá sale)"""
        return self.sale_price if self.sale_price else self.base_price

    @property
    def discount_percent(self):
        """Phần trăm giảm giá"""
        if self.sale_price and self.base_price > self.sale_price:
            return int(((self.base_price - self.sale_price) / self.base_price) * 100)
        return 0

    @property
    def is_on_sale(self):
        return bool(self.sale_price and self.sale_price < self.base_price)

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def is_in_stock(self):
        return self.variants.filter(stock__gt=0).exists()


class Color(models.Model):
    """Màu sắc"""
    name = models.CharField(max_length=50, verbose_name="Tên màu")
    hex_code = models.CharField(max_length=7, verbose_name="Mã màu HEX", blank=True)

    class Meta:
        verbose_name = 'Màu sắc'
        verbose_name_plural = 'Màu sắc'

    def __str__(self):
        return self.name


class Size(models.Model):
    """Kích thước"""
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'),
        ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL'),
        ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'),
        ('32', '32'), ('33', '33'), ('34', '34'), ('36', '36'),
    ]
    name = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name="Kích thước")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Kích thước'
        verbose_name_plural = 'Kích thước'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Biến thể sản phẩm (màu + size)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name="Sản phẩm")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Màu sắc")
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kích thước")
    stock = models.IntegerField(default=0, verbose_name="Tồn kho")
    sku = models.CharField(max_length=100, unique=True, blank=True, verbose_name="SKU")
    extra_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Giá thêm")

    class Meta:
        verbose_name = 'Biến thể'
        verbose_name_plural = 'Biến thể'
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        parts = [str(self.product)]
        if self.color:
            parts.append(self.color.name)
        if self.size:
            parts.append(self.size.name)
        return ' - '.join(parts)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{str(self.product.id)[:8]}-{self.color.name if self.color else 'NA'}-{self.size.name if self.size else 'NA'}"
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.product.current_price + self.extra_price

    @property
    def is_available(self):
        return self.stock > 0


class ProductImage(models.Model):
    """Ảnh sản phẩm"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Sản phẩm")
    image = models.ImageField(upload_to='products/', verbose_name="Ảnh")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Alt text")
    is_main = models.BooleanField(default=False, verbose_name="Ảnh chính")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Màu sắc")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Ảnh sản phẩm'
        verbose_name_plural = 'Ảnh sản phẩm'
        ordering = ['-is_main', 'order']

    def __str__(self):
        return f"Ảnh của {self.product.name}"

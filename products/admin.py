from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductVariant, ProductImage, Color, Size


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image_preview', 'image', 'alt_text', 'is_main', 'color', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:60px;height:70px;object-fit:cover;border-radius:4px;border:1px solid #ccc;" />', obj.image.url)
        return 'Chưa có'
    image_preview.short_description = 'Ảnh hiện tại'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 3
    fields = ('color', 'size', 'stock', 'sku', 'extra_price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'sale_price', 'is_active',
                    'is_featured', 'is_new_arrival', 'is_best_seller', 'total_sold', 'main_image_preview')
    list_filter = ('is_active', 'is_featured', 'is_new_arrival', 'is_best_seller', 'category', 'gender')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'is_new_arrival', 'is_best_seller')
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('total_sold', 'created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('name', 'slug', 'category', 'gender', 'description')}),
        ('Giá', {'fields': ('base_price', 'sale_price')}),
        ('Chất liệu & Bảo quản', {'fields': ('material', 'care_instructions')}),
        ('Trạng thái', {'fields': ('is_active', 'is_featured', 'is_new_arrival', 'is_best_seller')}),
        ('Thống kê', {'fields': ('total_sold', 'created_at', 'updated_at')}),
    )

    def main_image_preview(self, obj):
        img = obj.main_image
        if img:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />', img.image.url)
        return 'Chưa có ảnh'
    main_image_preview.short_description = '  Ảnh'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'color_preview')

    def color_preview(self, obj):
        if obj.hex_code:
            return format_html('<div style="width:30px;height:30px;background:{};border:1px solid #ccc;border-radius:50%;"></div>', obj.hex_code)
        return ''
    color_preview.short_description = 'Preview'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'stock', 'sku', 'is_available')
    list_filter = ('color', 'size')
    search_fields = ('product__name', 'sku')
    list_editable = ('stock',)

    def is_available(self, obj):
        if obj.stock > 0:
            return format_html('<span style="color:green;">&#10003; Còn hàng ({})</span>', obj.stock)
        return format_html('<span style="color:red;">&#10007; Hết hàng</span>')
    is_available.short_description = 'Tình trạng'

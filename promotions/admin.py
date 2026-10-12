from django.contrib import admin
from django.utils.html import format_html
from .models import Coupon, Banner


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'minimum_order', 'used_count', 'max_uses', 'is_active', 'valid_from', 'valid_to')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code', 'description')
    list_editable = ('is_active',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'preview')
    list_editable = ('is_active', 'order')

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />', obj.image.url)
        return ''
    preview.short_description = 'Preview'

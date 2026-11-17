from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'order_link', 'amount_display', 'status_badge',
        'receipt_thumb', 'qr_link', 'transaction_id', 'bank_name', 'created_at', 'confirmed_at'
    )
    list_filter = ('status', 'bank_name', 'created_at')
    search_fields = ('order__order_number', 'transaction_id', 'bank_name', 'notes')
    readonly_fields = ('id', 'created_at', 'receipt_preview')
    ordering = ('-created_at',)
    list_per_page = 25
    actions = ['confirm_payments', 'reject_payments']

    fieldsets = (
        ('Thông tin thanh toán', {
            'fields': ('id', 'order', 'amount', 'status')
        }),
        ('Giao dịch & Ngân hàng', {
            'fields': ('bank_name', 'transaction_id', 'notes')
        }),
        ('Biên lai chuyển khoản', {
            'fields': ('receipt_image', 'receipt_preview')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )

    def order_link(self, obj):
        return f"Đơn #{obj.order.order_number}"
    order_link.short_description = 'Đơn hàng'

    def amount_display(self, obj):
        return format_html('<strong>{} VNĐ</strong>', f"{obj.amount:,.0f}")
    amount_display.short_description = 'Số tiền'

    def status_badge(self, obj):
        colors = {
            'pending': ('#f59e0b', '⏳ Chờ TT'),
            'uploaded': ('#3b82f6', '📷 Đã gửi bill'),
            'confirmed': ('#10b981', '✅ Đã duyệt'),
            'failed': ('#ef4444', '❌ Thất bại'),
        }
        color, text = colors.get(obj.status, ('#6b7280', obj.status))
        return format_html(
            '<span style="background:{};color:white;padding:3px 8px;border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Trạng thái'

    def receipt_thumb(self, obj):
        if obj.receipt_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width:45px;height:45px;object-fit:cover;border-radius:4px;border:1px solid #ddd;" title="Nhấn để xem ảnh lớn"/>'
                '</a>',
                obj.receipt_image.url, obj.receipt_image.url
            )
        return format_html('<span style="color:#aaa;font-size:12px;">Chưa có</span>')
    receipt_thumb.short_description = 'Biên lai'

    def qr_link(self, obj):
        qr_url = reverse('payment_qr', kwargs={'order_id': obj.order.id})
        return format_html(
            '<a href="{}" target="_blank" style="background:#059669;color:white;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:600;text-decoration:none;">'
            '📱 Xem QR'
            '</a>',
            qr_url
        )
    qr_link.short_description = 'Mã QR'

    def receipt_preview(self, obj):
        if obj.receipt_image:
            return format_html(
                '<div style="margin-top:10px;">'
                '<a href="{}" target="_blank"><img src="{}" style="max-width:320px;max-height:400px;border-radius:8px;border:1px solid #ccc;"/></a>'
                '<p style="color:#666;font-size:12px;margin-top:4px;">Nhấn vào ảnh để xem kích thước đầy đủ trong tab mới</p>'
                '</div>',
                obj.receipt_image.url, obj.receipt_image.url
            )
        return 'Chưa có ảnh biên lai'
    receipt_preview.short_description = 'Xem trước biên lai'

    def confirm_payments(self, request, queryset):
        count = 0
        for p in queryset:
            p.status = 'confirmed'
            p.confirmed_at = timezone.now()
            p.save()
            if p.order.status in ['pending', 'confirmed']:
                p.order.status = 'processing'
                p.order.save()
            count += 1
        self.message_user(request, f'✅ Đã duyệt thành công {count} khoản thanh toán. Đơn hàng chuyển sang Đang đóng gói.')
    confirm_payments.short_description = '✅ Duyệt thanh toán & chuyển đơn sang đóng gói'

    def reject_payments(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'❌ Đã từ chối {updated} khoản thanh toán.')
    reject_payments.short_description = '❌ Đánh dấu thanh toán thất bại'

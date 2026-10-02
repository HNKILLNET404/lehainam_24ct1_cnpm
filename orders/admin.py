from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'color_name', 'size_name', 'unit_price', 'quantity', 'total_price_display')
    fields = ('product_name', 'color_name', 'size_name', 'unit_price', 'quantity', 'total_price_display')
    can_delete = False

    def total_price_display(self, obj):
        return format_html('<strong>{} VNĐ</strong>', f"{obj.total_price:,.0f}")
    total_price_display.short_description = 'Thành tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'full_name', 'phone', 'status_badge',
        'payment_badge', 'total_display', 'item_count', 'qr_action_link', 'created_at'
    )
    list_filter = ('status', 'shipping_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'email', 'user__email')
    readonly_fields = ('id', 'order_number', 'created_at', 'updated_at', 'qr_action_link', 'order_summary_box')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    list_per_page = 25
    ordering = ('-created_at',)

    fieldsets = (
        ('📋 Thông tin đơn hàng', {
            'fields': ('id', 'order_number', 'user', 'status', 'qr_action_link', 'notes', 'order_summary_box')
        }),
        ('🚚 Thông tin giao hàng', {
            'fields': (
                'full_name', 'phone', 'email',
                ('province', 'district', 'ward'), 'street_address',
                'shipping_method'
            )
        }),
        ('💰 Thanh toán', {
            'fields': ('subtotal', 'discount_amount', 'shipping_fee', 'total', 'coupon_code')
        }),
        ('🕐 Thời gian', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_confirmed', 'mark_processing', 'mark_shipping', 'mark_delivered', 'mark_cancelled']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('items', 'payment')

    def status_badge(self, obj):
        colors = {
            'pending': ('#f59e0b', '⏳'),
            'confirmed': ('#3b82f6', '✅'),
            'processing': ('#8b5cf6', '📦'),
            'shipping': ('#6366f1', '🚚'),
            'delivered': ('#10b981', '🎉'),
            'cancelled': ('#ef4444', '❌'),
            'refunded': ('#6b7280', '↩️'),
        }
        color, icon = colors.get(obj.status, ('#6b7280', '?'))
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">'
            '{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = 'Trạng thái'

    def payment_badge(self, obj):
        payment = getattr(obj, 'payment', None)
        if not payment:
            return format_html('<span style="color:#f59e0b;font-size:11px;">⚠ Chưa TT</span>')
        p_colors = {
            'pending': ('#f59e0b', 'Chờ TT'),
            'uploaded': ('#3b82f6', 'Chờ xác nhận'),
            'confirmed': ('#10b981', 'Đã TT'),
            'failed': ('#ef4444', 'Thất bại'),
        }
        color, label = p_colors.get(payment.status, ('#6b7280', payment.status))
        return format_html(
            '<span style="color:{};font-size:11px;font-weight:600;">{}</span>',
            color, label
        )
    payment_badge.short_description = 'Thanh toán'

    def total_display(self, obj):
        return format_html('<strong style="color:#111">{}đ</strong>', f"{obj.total:,.0f}")
    total_display.short_description = 'Tổng'

    def item_count(self, obj):
        count = obj.items.count()
        return format_html('<span style="background:#f3f4f6;padding:2px 8px;border-radius:10px;">{} SP</span>', count)
    item_count.short_description = 'SL'

    def qr_action_link(self, obj):
        qr_url = reverse('payment_qr', kwargs={'order_id': obj.id})
        return format_html(
            '<a href="{}" target="_blank" style="background:#111;color:white;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600;text-decoration:none;display:inline-block;">'
            '📱 Xem QR Code'
            '</a>',
            qr_url
        )
    qr_action_link.short_description = 'Trang QR'

    def order_summary_box(self, obj):
        items = obj.items.all()
        rows = ''
        for item in items:
            rows += f'''
            <tr>
                <td style="padding:6px 10px;">{item.product_name}</td>
                <td style="padding:6px 10px;color:#888;">{item.color_name} / {item.size_name}</td>
                <td style="padding:6px 10px;text-align:center;">×{item.quantity}</td>
                <td style="padding:6px 10px;text-align:right;font-weight:600;">{item.unit_price:,.0f}đ</td>
                <td style="padding:6px 10px;text-align:right;font-weight:600;">{item.total_price:,.0f}đ</td>
            </tr>'''
        return format_html('''
            <div style="border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;margin-top:8px;">
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <thead>
                        <tr style="background:#f9fafb;">
                            <th style="padding:8px 10px;text-align:left;">Sản phẩm</th>
                            <th style="padding:8px 10px;text-align:left;color:#888;">Phân loại</th>
                            <th style="padding:8px 10px;text-align:center;">SL</th>
                            <th style="padding:8px 10px;text-align:right;">Đơn giá</th>
                            <th style="padding:8px 10px;text-align:right;">Thành tiền</th>
                        </tr>
                    </thead>
                    <tbody>{}
                    </tbody>
                    <tfoot style="border-top:2px solid #e5e7eb;background:#f9fafb;">
                        <tr>
                            <td colspan="4" style="padding:8px 10px;text-align:right;">Tạm tính:</td>
                            <td style="padding:8px 10px;text-align:right;">{}đ</td>
                        </tr>
                        <tr>
                            <td colspan="4" style="padding:4px 10px;text-align:right;color:green;">Giảm giá:</td>
                            <td style="padding:4px 10px;text-align:right;color:green;">-{}đ</td>
                        </tr>
                        <tr>
                            <td colspan="4" style="padding:4px 10px;text-align:right;">Phí ship:</td>
                            <td style="padding:4px 10px;text-align:right;">{}đ</td>
                        </tr>
                        <tr style="font-size:15px;font-weight:bold;">
                            <td colspan="4" style="padding:8px 10px;text-align:right;">TỔNG CỘNG:</td>
                            <td style="padding:8px 10px;text-align:right;color:#111;">{}đ</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        ''', format_html(rows), f"{obj.subtotal:,.0f}", f"{obj.discount_amount:,.0f}", f"{obj.shipping_fee:,.0f}", f"{obj.total:,.0f}")
    order_summary_box.short_description = 'Chi tiết đơn hàng'

    # ── ACTIONS ──
    def mark_confirmed(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'✅ Đã xác nhận {updated} đơn hàng.')
    mark_confirmed.short_description = '✅ Xác nhận đơn (pending → confirmed)'

    def mark_processing(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='processing')
        self.message_user(request, f'📦 Đã chuyển {updated} đơn sang đang đóng gói.')
    mark_processing.short_description = '📦 Đóng gói (confirmed → processing)'

    def mark_shipping(self, request, queryset):
        updated = queryset.filter(status='processing').update(status='shipping', shipped_at=timezone.now())
        self.message_user(request, f'🚚 Đã bàn giao {updated} đơn cho vận chuyển.')
    mark_shipping.short_description = '🚚 Giao vận (processing → shipping)'

    def mark_delivered(self, request, queryset):
        updated = queryset.filter(status='shipping').update(status='delivered', delivered_at=timezone.now())
        self.message_user(request, f'🎉 Đã hoàn thành {updated} đơn hàng.')
    mark_delivered.short_description = '🎉 Hoàn thành (shipping → delivered)'

    def mark_cancelled(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='cancelled')
        self.message_user(request, f'❌ Đã hủy {updated} đơn hàng.')
    mark_cancelled.short_description = '❌ Hủy đơn'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'color_name', 'size_name', 'unit_price', 'quantity', 'total_price_display')
    search_fields = ('order__order_number', 'product_name')
    list_per_page = 50

    def total_price_display(self, obj):
        return f'{obj.total_price:,.0f}đ'
    total_price_display.short_description = 'Thành tiền'

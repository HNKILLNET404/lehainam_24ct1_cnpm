from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Q
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'role', 'vai_tro', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('role', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'avatar')}),
        ('Phân quyền & Vai trò', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Ngày quan trọng', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )

    def vai_tro(self, obj):
        if obj.role == 'admin' or obj.is_superuser:
            return format_html('<span style="background:#dc2626;color:#fff;padding:3px 10px;border-radius:12px;font-weight:bold;font-size:11px;">👑 Admin Quản trị</span>')
        if obj.role == 'staff' or obj.is_staff:
            return format_html('<span style="background:#2563eb;color:#fff;padding:3px 10px;border-radius:12px;font-weight:bold;font-size:11px;">👔 Nhân viên (Staff)</span>')
        return format_html('<span style="background:#059669;color:#fff;padding:3px 10px;border-radius:12px;font-weight:bold;font-size:11px;">👤 Khách hàng</span>')
    vai_tro.short_description = 'Phù hiệu'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['summary_total'] = User.objects.count()
        extra_context['summary_admin'] = User.objects.filter(Q(role='admin') | Q(is_superuser=True)).count()
        extra_context['summary_staff'] = User.objects.filter(role='staff').count()
        extra_context['summary_customer'] = User.objects.filter(role='customer').count()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'province', 'district', 'is_default')
    list_filter = ('province', 'is_default')
    search_fields = ('user__email', 'full_name', 'phone')

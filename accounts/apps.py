from django.apps import AppConfig
from django import forms


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib import admin
        from django.contrib.admin.forms import AdminAuthenticationForm

        class CustomAdminAuthenticationForm(AdminAuthenticationForm):
            def confirm_login_allowed(self, user):
                super(AdminAuthenticationForm, self).confirm_login_allowed(user)
                # Cho phép đăng nhập nếu là superuser, staff, hoặc role in ('admin', 'staff')
                if not (user.is_staff or user.is_superuser or getattr(user, 'role', '') in ('admin', 'staff')):
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        def custom_has_permission(request):
            u = request.user
            if not u or not u.is_authenticated or not u.is_active:
                return False
            return u.is_superuser or u.is_staff or getattr(u, 'role', '') in ('admin', 'staff')

        admin.site.login_form = CustomAdminAuthenticationForm
        admin.site.has_permission = custom_has_permission

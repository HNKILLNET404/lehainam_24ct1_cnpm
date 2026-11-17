from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User model"""
    ROLE_CHOICES = (
        ('admin', 'Quản trị viên (Admin)'),
        ('staff', 'Nhân viên (Staff)'),
        ('customer', 'Khách hàng (Customer)'),
    )

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Ảnh đại diện")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    is_email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name="Vai trò")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_employee(self):
        return self.role == 'staff' or (self.is_staff and not self.is_superuser)

    @property
    def is_customer(self):
        return self.role == 'customer' and not self.is_superuser and not self.is_staff

    def save(self, *args, **kwargs):
        # Tự động đồng bộ chuẩn hóa phân quyền:
        # - Admin: is_superuser = True, is_staff = False (không trùng 1 với nhân viên trong CSDL)
        # - Nhân viên: is_staff = True, is_superuser = False
        # - Khách hàng: is_staff = False, is_superuser = False
        if self.role == 'admin' or self.is_superuser:
            self.role = 'admin'
            self.is_superuser = True
            self.is_staff = False
        elif self.role == 'staff' or self.is_staff:
            self.role = 'staff'
            self.is_staff = True
            self.is_superuser = False
        else:
            self.role = 'customer'
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    @property
    def default_address(self):
        return self.addresses.filter(is_default=True).first()


class Address(models.Model):
    """User shipping address"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="Người dùng")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    province = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    street_address = models.CharField(max_length=255, verbose_name="Địa chỉ cụ thể")
    is_default = models.BooleanField(default=False, verbose_name="Địa chỉ mặc định")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Địa chỉ'
        verbose_name_plural = 'Địa chỉ'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.street_address}, {self.ward}, {self.district}, {self.province}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Remove default from other addresses of same user
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

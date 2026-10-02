from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Address

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Đăng ký tài khoản mới"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Email của bạn'
        })
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Họ'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Tên'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Số điện thoại (tùy chọn)'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Mật khẩu'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Xác nhận mật khẩu'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # use email as username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('phone'):
            user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Đăng nhập"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Email của bạn'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Mật khẩu'
        })
    )


class ProfileForm(forms.ModelForm):
    """Cập nhật hồ sơ cá nhân"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'date_of_birth', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
        }


class AddressForm(forms.ModelForm):
    """Thêm/sửa địa chỉ giao hàng"""
    class Meta:
        model = Address
        fields = ('full_name', 'phone', 'province', 'district', 'ward', 'street_address', 'is_default')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'placeholder': 'Họ và tên'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'placeholder': 'Số điện thoại'}),
            'province': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'placeholder': 'Tỉnh/Thành phố'}),
            'district': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'placeholder': 'Quận/Huyện'}),
            'ward': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'placeholder': 'Phường/Xã'}),
            'street_address': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black', 'placeholder': 'Số nhà, tên đường'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
        }

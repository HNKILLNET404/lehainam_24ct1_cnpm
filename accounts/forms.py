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
    full_name = forms.CharField(
        max_length=100,
        label='Họ và tên',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Họ và tên của bạn'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        label='Số điện thoại',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Số điện thoại (tùy chọn)'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Nhập lại password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black',
            'placeholder': 'Nhập lại password'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # use email as username
        
        full_name = self.cleaned_data.get('full_name', '').strip()
        parts = full_name.rsplit(' ', 1)
        if len(parts) == 2:
            user.first_name = parts[0]
            user.last_name = parts[1]
        else:
            user.first_name = full_name
            user.last_name = ''

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

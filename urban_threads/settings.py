# =============================================================================
# URBAN THREADS — Website Bán Thời Trang Streetwear
# =============================================================================
# PHIA SAU (Backend Framework): Django 5.1.1 | Python 3.10+
# PHIA TRUOC (Frontend Framework): Tailwind CSS v3 (CDN) + Alpine.js v3 (CDN)
# CO SO DU LIEU (Database): SQLite — file: db.sqlite3
# CONG THANH TOAN (Payment): VietQR API (Napas247)
# KIEN TRUC (Architecture): MVT — Model / View / Template
# =============================================================================

from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'crispy_forms',
    'crispy_tailwind',
    # Local apps
    'accounts',
    'products',
    'cart',
    'orders',
    'payments',
    'reviews',
    'wishlists',
    'promotions',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.middleware.CartMiddleware',
]

ROOT_URLCONF = 'urban_threads.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_processor',
                'products.context_processors.categories_processor',
            ],
            'builtins': [
                'products.templatetags.currency_filters',
            ],
        },
    },
]

WSGI_APPLICATION = 'urban_threads.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = 'Urban Threads <noreply@urbanthreads.com>'

# QR Payment settings
BANK_ID = config('BANK_ID', default='970422')  # Mã BIN hoặc mã ngân hàng (VCB, TCB, MB, ACB...)
BANK_NAME = config('BANK_NAME', default='')    # Tên ngân hàng (tự động nhận diện nếu để trống)
BANK_ACCOUNT_NO = config('BANK_ACCOUNT_NO', default='1234567890')
BANK_ACCOUNT_NAME = config('BANK_ACCOUNT_NAME', default='URBAN THREADS STORE')
BANK_TEMPLATE = config('BANK_TEMPLATE', default='compact')

# Free shipping threshold (VND)
FREE_SHIPPING_THRESHOLD = config('FREE_SHIPPING_THRESHOLD', default=500000, cast=int)

# Shipping prices
SHIPPING_STANDARD = 30000  # 30k
SHIPPING_EXPRESS = 50000   # 50k
SHIPPING_SAME_DAY = 80000  # 80k

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

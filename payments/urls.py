from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:order_id>/qr/', views.payment_qr_view, name='payment_qr'),
    path('<uuid:payment_id>/upload-receipt/', views.upload_receipt, name='upload_receipt'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('<uuid:order_id>/', views.order_detail_view, name='order_detail'),
    path('<uuid:order_id>/cancel/', views.order_cancel_view, name='order_cancel'),
    path('<uuid:order_id>/thank-you/', views.order_thank_you, name='order_thank_you'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search_view, name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('size-guide/', views.size_guide_view, name='size_guide'),
    path('returns/', views.returns_policy_view, name='returns'),
    path('faq/', views.faq_view, name='faq'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('cookie-policy/', views.cookie_policy_view, name='cookie_policy'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
]

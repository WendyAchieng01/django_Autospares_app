# paymentdaraja/urls.py

from django.urls import path
from . import views

app_name = 'paymentdaraja'

urlpatterns = [
    path('payment_index/', views.payment_index, name='payment_index'),
    path('daraja/stk-push', views.payment_stk_push_callback, name='mpesa_stk_push_callback'),
    path('payment_page/', views.payment_page, name='payment_page'),
    path('payment_success/', views.payment_success, name='payment_success'),
]

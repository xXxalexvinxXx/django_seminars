from django.urls import path
from . import views

urlpatterns = [
    path('client/<int:client_id>/products/', views.client_products, name='client_products'),
]
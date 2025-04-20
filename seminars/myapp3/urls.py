from django.urls import path
from . import views

app_name = 'myapp3'

urlpatterns = [
    path('clients/<int:client_id>/products/', views.ClientOrderedProductsView.as_view(), name='client_ordered_products'),
] 
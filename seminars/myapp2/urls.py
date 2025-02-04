from django.urls import path
from . import views

app_name = 'myapp2'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.ClientOrderDetailView.as_view(), name='order_detail'),
]
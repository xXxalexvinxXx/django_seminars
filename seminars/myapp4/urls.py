from django.urls import path
from . import views

app_name = 'myapp4'

urlpatterns = [
    # Маршруты для работы с фотографиями товаров
    path('photos/', views.ProductPhotosListView.as_view(), name='product_photos_list'),
    path('products/<int:product_id>/photos/add/', views.ProductPhotoCreateView.as_view(), name='add_product_photo'),
    path('photos/<int:pk>/delete/', views.ProductPhotoDeleteView.as_view(), name='delete_product_photo'),
    path('photos/<int:pk>/set-main/', views.SetMainPhotoView.as_view(), name='set_main_photo'),
] 
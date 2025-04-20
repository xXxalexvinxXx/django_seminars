from django.contrib import admin
from .models import ProductPhoto

@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('product__name',)
    date_hierarchy = 'created_at'
    list_per_page = 20

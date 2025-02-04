from django.contrib import admin
from .models import Client, Order

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'registration_date')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'total_amount', 'status')
    list_filter = ('status',)
from django import forms
from .models import Client, Product, Order

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address', 'personal_discount']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity',
                 'discount', 'discount_type', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'status']

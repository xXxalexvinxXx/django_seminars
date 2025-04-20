from django import forms
from .models import ProductPhoto
from myapp2.models import Product

class ProductPhotoForm(forms.ModelForm):
    """
    Форма для загрузки фотографии товара
    """
    class Meta:
        model = ProductPhoto
        fields = ['product', 'photo', 'is_main']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        
        if self.product_id:
            # Если продукт известен, скрываем его выбор в форме
            self.instance.product_id = self.product_id
            del self.fields['product']
        else:
            # Если продукт не известен, включаем поле выбора продукта
            self.fields['product'].queryset = Product.objects.all().order_by('name')
            self.fields['product'].empty_label = 'Выберите продукт' 
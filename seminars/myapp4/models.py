from django.db import models
from myapp2.models import Product

class ProductPhoto(models.Model):
    """
    Модель для хранения фотографий продукта
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Товар'
    )
    photo = models.ImageField(
        'Фотография',
        upload_to='product_photos/%Y/%m/',
        help_text='Загрузите фотографию товара'
    )
    is_main = models.BooleanField(
        'Основное фото',
        default=False,
        help_text='Отметьте, если это основное фото товара'
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'
        ordering = ['-is_main', '-created_at']
    
    def __str__(self):
        return f"Фото для {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Если фото помечено как основное, убрать это свойство у других фото товара
        if self.is_main:
            ProductPhoto.objects.filter(
                product=self.product, 
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
    EmailValidator
)
from django.db.models import F, Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import re

User = get_user_model()


def validate_non_empty(value):
    if not value.strip():
        raise ValidationError("Это поле не может быть пустым")


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[
            validate_non_empty,
            RegexValidator(
                regex=r'^(\+?\d{1})?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',
                message='Введите номер в формате: +X (XXX) XXX-XX-XX'
            )
        ]
    )
    email = models.EmailField(
        'Электронная почта',
        validators=[
            EmailValidator(message="Введите корректный email адрес"),
            validate_non_empty
        ],
        unique=True
    )
    personal_discount = models.DecimalField(
        'Персональная скидка',
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    registration_date = models.DateTimeField('Дата регистрации', auto_now_add=True)

    def clean(self):
        # Нормализация номера телефона
        if self.phone:
            self.phone = re.sub(r'[^\d+]', '', self.phone)
            if len(self.phone) == 11 and self.phone.startswith('8'):
                self.phone = '+7' + self.phone[1:]

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.phone})"


class Product(models.Model):
    DISCOUNT_TYPES = (
        ('add', 'Складывается с персональной'),
        ('max', 'Максимальная из доступных'),
        ('override', 'Перекрывает все скидки'),
    )

    name = models.CharField(
        'Название',
        max_length=100,
        validators=[
            validate_non_empty,
            RegexValidator(
                regex=r'^[a-zA-Zа-яА-ЯёЁ0-9\-\s]+$',
                message='Название может содержать только буквы, цифры и дефис'
            )
        ]
    )
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField('Количество на складе', default=0)
    discount = models.DecimalField(
        'Скидка',
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    discount_type = models.CharField(
        'Тип скидки',
        max_length=10,
        choices=DISCOUNT_TYPES,
        default='max'
    )
    added_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-added_date']

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен')
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент'
    )
    total_amount = models.DecimalField(
        'Сумма заказа',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    order_date = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):
        return f"Заказ №{self.id} - {self.client}"

    def update_total(self):
        self.total_amount = self.items.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0
        self.save(update_fields=['total_amount'])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        default=1,
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    applied_discount = models.DecimalField(
        'Примененная скидка',
        max_digits=5,
        decimal_places=2,
        default=0
    )

    def clean(self):
        # Проверка доступного количества
        if self.quantity > self.product.quantity:
            raise ValidationError(
                f"Недостаточно товара. Доступно: {self.product.quantity}"
            )

        # Рассчет скидки
        client_discount = self.order.client.personal_discount
        product_discount = self.product.discount

        if self.product.discount_type == 'add':
            total_discount = client_discount + product_discount
            self.applied_discount = min(total_discount, 100)
        elif self.product.discount_type == 'max':
            self.applied_discount = max(client_discount, product_discount)
        else:  # override
            self.applied_discount = product_discount

        # Применение скидки к цене
        self.price = self.product.price * (100 - self.applied_discount) / 100

        if self.price < 0:
            raise ValidationError("Цена товара не может быть отрицательной")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Резервирование товара
        self.product.quantity -= self.quantity
        self.product.save()

    def delete(self, *args, **kwargs):
        # Возврат товара на склад
        if self.quantity > self.product.quantity + self.quantity:
            raise ValidationError("Невозможно вернуть больше товара чем было зарезервировано")
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    instance.order.update_total()
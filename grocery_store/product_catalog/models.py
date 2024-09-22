from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название катгории', max_length=100)
    slug = models.SlugField('slug', max_length=200, unique=True)
    image = models.ImageField(
        upload_to='categories//%Y/%m/%d',
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        verbose_name='Категория родитль',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    # Связь с родительской категорией, позволяющая создавать иерархическую структуру

    def __str__(self):
        return self.name  # Для удобного отображения названия категории


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )
    name = models.CharField('Название товара', max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        'Фото',
        upload_to='products/%Y/%m/%d',
        blank=True,
        null=True,
    )
    image_small = models.ImageField(
        'Маленькое фото',
        upload_to='products/small/%Y/%m/%d',
        blank=True,
        null=True,
    )
    image_medium = models.ImageField(
        'Среднее фото',
        upload_to='products/medium/%Y/%m/%d',
        blank=True,
        null=True,
    )
    image_large = models.ImageField(
        'Большое фото',
        upload_to='products/large/%Y/%m/%d',
        blank=True,
        null=True,
    )
    description = models.TextField('Описание товара', blank=True)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
    )  # Для хранения денежных сумм лучше использовать Decimal а не float
    available = models.BooleanField('В наличии', default=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        verbose_name='Клиент',
    )
    products = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Продукты',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'user',
                    'products',
                ),
                name='ShoppingCart',
            )
        ]

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
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
    image = models.ImageField('Фото', upload_to='products/%Y/%m/%d', blank=True)
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

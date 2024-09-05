from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название категории', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse(
            'product_catalog:product_list_by_category',
            args=[self.slug],
        )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

        def __str__(self):
            return self.name


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

    def get_absolute_url(self):
        return reverse(
            'product_catalog:product_detail',
            args=[self.id, self.slug],
        )

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

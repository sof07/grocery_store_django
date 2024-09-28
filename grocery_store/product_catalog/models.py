from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from product_catalog.utils import unique_slugify

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('slug', max_length=200, unique=True)
    image = models.ImageField(
        upload_to='categories/%Y/%m/%d',
        blank=True,
        null=True,
    )
    parent = TreeForeignKey(
        'self',
        related_name='subcategories',
        verbose_name='Категория родитель',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория товара',
    )
    name = models.CharField('Название товара', max_length=200)
    slug = models.SlugField('Слаг', max_length=200)
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
    currency = models.CharField(
        'Денежная единица',
        max_length=4,
        default='руб',
    )
    unit_of_measurement = models.CharField(
        'Единица измерения',
        max_length=6,
        default='кг',
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

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Корзина пользователя',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return (
            f'{self.product.name} x {self.quantity} {self.product.unit_of_measurement}'
        )

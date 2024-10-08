# Generated by Django 5.1.1 on 2024-09-23 10:17

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='slug')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/%Y/%m/%d')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='product_catalog.category', verbose_name='Категория родитель')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название товара')),
                ('slug', models.SlugField(max_length=200)),
                ('image_small', models.ImageField(blank=True, null=True, upload_to='products/small/%Y/%m/%d', verbose_name='Маленькое фото')),
                ('image_medium', models.ImageField(blank=True, null=True, upload_to='products/medium/%Y/%m/%d', verbose_name='Среднее фото')),
                ('image_large', models.ImageField(blank=True, null=True, upload_to='products/large/%Y/%m/%d', verbose_name='Большое фото')),
                ('description', models.TextField(blank=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('available', models.BooleanField(default=True, verbose_name='В наличии')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product_catalog.category')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product_catalog.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalog.product')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='product_cat_id_4742c5_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='product_cat_name_3c49a2_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-created'], name='product_cat_created_19470e_idx'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-05 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]

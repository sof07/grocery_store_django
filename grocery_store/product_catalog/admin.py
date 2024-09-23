from django.contrib import admin
from product_catalog.models import Category, Product, Cart, CartItem
from django_mptt_admin.admin import DjangoMpttAdmin
from django.forms import TextInput, Textarea
from django.db import models


class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    mptt_level_indent = 20


class CartItemInline(admin.TabularInline):
    """
    Класс позволяет просматривать товары в корзине пользователя
    """

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    model = CartItem
    extra = 0  # Убираем пустые поля для добавления нового товара в корзину
    fields = (
        'product',
        'quantity',
        'unit_of_measurement',
        'total_cost',
    )
    readonly_fields = (
        'product',
        'total_cost',
        'unit_of_measurement',
    )

    def unit_of_measurement(self, obj):
        return obj.product.unit_of_measurement

    def total_cost(self, obj):  # Дополнительное поле которого нет в модели
        return f'{obj.product.price * obj.quantity} {obj.product.currency}'

    total_cost.short_description = 'Общая стоимость'
    unit_of_measurement.short_description = 'Еденица измерения'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'created_at',
        'total_cost',
    )
    inlines = [CartItemInline]

    def total_cost(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

    total_cost.short_description = 'Общая стоимость'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '5'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 5})},
    }
    list_display = [
        'name',
        'slug',
        'price',
        'currency',
        'unit_of_measurement',
        'available',
        'category',
        'image_small',
        'image_medium',
        'image_large',
        'created',
        'updated',
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = [
        'price',
        'currency',
        'unit_of_measurement',
        'available',
        'category',
        'slug',
        'image_small',
        'image_medium',
        'image_large',
    ]
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 5


admin.site.empty_value_display = 'Не задано'
admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Магазин продуктов'

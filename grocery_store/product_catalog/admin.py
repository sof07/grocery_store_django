from django.contrib import admin
from product_catalog.models import Category, Product, Cart, CartItem
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(
            parent__isnull=True
        )  # Только корневые категории


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('name', 'parent', 'slug', 'image', 'get_subcategories_count')
    search_fields = ('name',)
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def get_subcategories_count(self, obj):
        return obj.subcategories.count()

    get_subcategories_count.short_description = 'Количество подкатегорий'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'category',
        'image_small',
        'image_medium',
        'image_large',
        'created',
        'updated',
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'category']
    prepopulated_fields = {'slug': ('name',)}


admin.site.empty_value_display = 'Не задано'

from django.contrib import admin
from product_catalog.models import Category, Product


class CategoryInlane(admin.TabularInline):
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-панель модели категорий
    """

    list_display = ('id', 'name', 'slug')
    list_display_links = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    # fieldsets = (
    #     ('Основная информация', {'fields': ('name', 'slug', 'parent')}),
    #     ('Описание', {'fields': ('description',)}),
    # )
    # prepopulated_fields = {'slug': ('name',)}
    # inlines = [CategoryInlane]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated',
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.

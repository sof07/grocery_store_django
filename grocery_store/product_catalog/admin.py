from django.contrib import admin
from product_catalog.models import Category, Product
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
    list_display = ('name', 'parent', 'slug', 'get_subcategories_count')
    search_fields = ('name',)
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def get_subcategories_count(self, obj):
        return obj.subcategories.count()

    get_subcategories_count.short_description = 'Количество подкатегорий'


# class CategoryInlane(admin.TabularInline):
#     model = Category


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     """
#     Админ-панель модели категорий
#     """

#     list_display = ('id', 'name', 'slug')
#     list_display_links = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}


#     # fieldsets = (
#     #     ('Основная информация', {'fields': ('name', 'slug', 'parent')}),
#     #     ('Описание', {'fields': ('description',)}),
#     # )
#     # prepopulated_fields = {'slug': ('name',)}
#     # inlines = [CategoryInlane]


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

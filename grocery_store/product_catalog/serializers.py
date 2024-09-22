from rest_framework import serializers
import base64

from .models import Category, Product, User, ShoppingCart

from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ReveuListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecrusiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializers = self.parent.parent.__class__(value, context=self.context)
        return serializers.data


class CategorySerializer_(serializers.ModelSerializer):
    class Meta:
        fields = ('name',)
        model = Category


class UserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'products')
        # ref_name = 'ReadOnlyUsers'


class ProductSerrializer(serializers.ModelSerializer):
    # category = CategorySerializer_()
    image = Base64ImageField(required=False, allow_null=True)
    slug = serializers.PrimaryKeyRelatedField(read_only=True)
    # category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'image',
            'description',
            'price',
            'category',
        )


class CategorySerializer(serializers.ModelSerializer):
    # subcategories = serializers.SerializerMethodField()
    subcategories = RecrusiveSerializer(required=False, many=True)
    parent = serializers.StringRelatedField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        list_serializer_class = ReveuListSerializer
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'parent',
            'image',
            'subcategories',
        )


class ProductsShopingCarsSerializer(serializers.ModelSerializer):
    image_small = Base64ImageField(required=False, allow_null=True)
    image_medium = Base64ImageField(required=False, allow_null=True)
    image_large = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'image_small',
            'image_medium',
            'image_large',
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    products = ProductsShopingCarsSerializer()  # разобраться с этим полм

    class Meta:
        model = ShoppingCart
        fields = ('products',)

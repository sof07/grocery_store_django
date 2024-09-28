import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Cart, CartItem, Category, Product, User


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
        ref_name = 'MyAppUser'


class CategorySerializer(serializers.ModelSerializer):
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


class ProductSerrializer(serializers.ModelSerializer):
    image_small = Base64ImageField(required=False, allow_null=True)
    image_medium = Base64ImageField(required=False, allow_null=True)
    image_large = Base64ImageField(required=False, allow_null=True)
    slug = serializers.PrimaryKeyRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'image_small',
            'image_medium',
            'image_large',
            'description',
            'price',
            'category',
            'currency',
            'unit_of_measurement',
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


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'product',
            'quantity',
        )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=False)
    user = serializers.StringRelatedField(read_only=True)
    total_sum = serializers.SerializerMethodField()
    number_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'number_of_products',
            'total_sum',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart

    def update(self, instance, validated_data):
        items_data = self.initial_data['items']
        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id:
                item = get_object_or_404(CartItem, id=item_id)
                if item_data.get('quantity') > 0:
                    item.quantity = item_data.get('quantity')
                    item.save()
                else:
                    item.delete()

        return instance

    def get_total_sum(self, obj):
        """
        Вычисляет стоимость товаров в корзине
        """
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

    def get_number_of_products(self, obj):
        """
        Вычисляет количество товаров в корзине
        """
        return obj.items.count()

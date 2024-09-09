from rest_framework import serializers

from .models import Category, Product


class ProductSerrializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            # 'image',
            'description',
            'price',
            'category',
        )


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

    def create(self, validated_data):
        parent = validated_data.pop('parent', None)
        category = Category.objects.create(parent=parent, **validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.save()
        return instance

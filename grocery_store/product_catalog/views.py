from rest_framework import viewsets

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerrializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerrializer

    def perform_create(self, serializer):
        serializer.save()  # Метод для создания товара

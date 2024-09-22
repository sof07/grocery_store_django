from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Category, Product, User, ShoppingCart
from .serializers import (
    CategorySerializer,
    ProductSerrializer,
    UserSerializer,
    ShoppingCartSerializer,
)
from rest_framework.response import Response
from rest_framework import status, permissions


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerrializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save()  # Метод для создания товара

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:
            return Response(
                {'errors': 'Продукт не существует'}, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            ShoppingCart.objects.create(user=request.user, products=product)
            response_serializer = ProductSerrializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

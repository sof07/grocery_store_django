from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, CartItem, Category, Product, User
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    CategorySerializer,
    ProductSerrializer,
    UserSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = [
        'get',
    ]
    pagination_class = None


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerrializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        return Response(
            {'error': 'Добавить продукт возможно только через панель администратора'},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        # Получаем продукт по ID
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'errors': 'Продукт не существует'}, status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем или создаём корзину пользователя
        cart, created = Cart.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            # Проверяем, существует ли уже товар в корзине
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            if not created:
                # Если товар уже есть, увеличиваем его количество
                cart_item.quantity += 1
                cart_item.save()

            total_price = sum(
                item.product.price * item.quantity for item in cart.items.all()
            )
            return Response(
                {'message': 'Товар добавлен в корзину', 'total_price': total_price},
                status=status.HTTP_201_CREATED,
            )

        elif request.method == 'DELETE':
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.delete()

                total_price = sum(
                    item.product.price * item.quantity for item in cart.items.all()
                )
                return Response(
                    {'message': 'Товар удалён из корзины', 'total_price': total_price},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except CartItem.DoesNotExist:
                return Response(
                    {'errors': 'Товар не найден в корзине'},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        # Ограничиваем выборку только корзиной для текущего пользователя
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()  # Возвращаем пустой queryset или дефолтный
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='cart_total')
    def cart_total(self, request):
        # Получаем корзину пользователя и её общую стоимость
        cart = Cart.objects.filter(user=request.user).first()
        total_price = 0

        if cart:
            total_price = sum(
                item.product.price * item.quantity for item in cart.items.all()
            )

        return Response({'total_price': total_price}, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Ограничиваем выборку только корзиной для текущего пользователя
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()  # Возвращаем пустой queryset или дефолтный
        return self.queryset.filter(cart__user=self.request.user)

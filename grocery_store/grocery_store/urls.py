from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import settings
from django.conf.urls.static import static


from django.urls import include, path

from product_catalog.views import (
    CategoryViewSet,
    ProductViewSet,
    UserViewSet,
    ShoppingCartViewSet,
)

# Создаётся роутер
router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='pategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'user', UserViewSet, basename='pser')
router.register(r'shopingcart', ShoppingCartViewSet, basename='shopingcart')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

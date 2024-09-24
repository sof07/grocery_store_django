from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


from django.urls import include, path

from product_catalog.views import (
    CategoryViewSet,
    ProductViewSet,
    UserViewSet,
    # ShoppingCartViewSet,
    CartViewSet,
    CartItemViewSet,
)

# Создаётся роутер
router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='pategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'user', UserViewSet, basename='pser')
# router.register(r'shopingcart', ShoppingCartViewSet, basename='shopingcart')
router.register(r'cart', CartViewSet)
# router.register(r'cartitem', CartItemViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description='Test description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path(
        'swagger<format>/',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

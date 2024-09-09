from django.contrib import admin
from rest_framework.routers import DefaultRouter

from django.urls import include, path

from product_catalog.views import CategoryViewSet, ProductViewSet

# Создаётся роутер
router = DefaultRouter()
router.register('category', CategoryViewSet, basename='Category')
router.register('product', ProductViewSet, basename='Product')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import cart_add, cart_detail, cart_remove
from shop.views import Product_detail,  index,  ProductList, ProductDetail, new_product, update_product, delete_product
from .api import ShopViewSet
router = DefaultRouter()
router.register(r'product', ShopViewSet, basename='product')



urlpatterns = [
    path("api/", include(router.urls)), 
    path('', index, name='index'),
    path("shop/", ProductList.as_view(), name="product-list"),
    path("new_product/", new_product, name="new_product"),
    path("shop/<slug:slug>/details/",
         ProductDetail.as_view(), name="product-details"),
    path("shop/<slug:slug>/update_product/",
         update_product, name="update_product"),
    path("shop/<slug:slug>/delete_product/",
         delete_product, name="delete_product"),
    path('Product/<slug:slug>/', Product_detail, name="product"),
    path("cart_detail", cart_detail, name="cart_detail"),
    path("add/<slug:slug>/", cart_add, name="cart_add"),
    path("remove/<int:product_id>/", cart_remove, name="cart_remove"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
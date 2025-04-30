from django.urls import path, include

# from rest_framework.routers import SimpleRouter, DefaultRouter
from product.views import (
    ProductViewSet,
    CategoryViewSet,
    ReviewViewSet,
    ProductImageViewSet,
)
from order.views import CartViewSet, OrderViewSet
from rest_framework_nested import routers
from order.views import CartItemViewSet, initiate_payment, payment_success


# router = SimpleRouter()
# router = DefaultRouter()
# router.register("products", ProductViewSet)
# router.register("categories", CategoryViewSet)


# urlpatterns = router.urls

# https//...api/products
# urlpatterns = [
#     path("", include(router.urls)),
#     path("products/", include("product.product_urls")),
#     path("categories/", include("product.category_urls")),
# ]


# for nested router:
router = routers.DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("carts", CartViewSet, basename="carts")
router.register("orders", OrderViewSet, basename="orders")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")
product_router.register("images", ProductImageViewSet, basename="product-images")
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-item")


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    path("payment/initiate/", initiate_payment, name="payment-initiate"),
    path("payment/success/", payment_success, name="payment-success"),
]

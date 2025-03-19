from django.urls import path, include

# from rest_framework.routers import SimpleRouter, DefaultRouter
from product.views import (
    ProductViewSet,
    CategoryViewSet,
    ReviewViewSet,
)
from order.views import CartViewSet
from rest_framework_nested import routers
from order.views import CartItemViewSet


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

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
]

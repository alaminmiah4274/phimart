from django.urls import path, include


# https//...api/products
urlpatterns = [
    path("products/", include("product.product_urls")),
    path("categories/", include("product.category_urls")),
]

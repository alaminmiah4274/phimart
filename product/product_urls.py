from django.urls import path
from product import views

urlpatterns = [
    path("", views.view_products, name="product-list"),
    path("<int:id>/", views.view_specific_product, name="specific_product"),
]

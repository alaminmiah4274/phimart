from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category
from rest_framework import status
from product.serializers import ProductSerializer

# Create your views here.
# def view_product(request):
#     return HttpResponse("Ok")


@api_view()
def view_products(request):
    return Response({"message": "product is ok"})


# @api_view()
# def view_specific_product(request, id):
#     # try:
#     #     product = Product.objects.get(pk=id)

#     #     product_dict = {"id": product.id, "name": product.name, "price": product.price}
#     #     return Response(product_dict)
#     # except Product.DoesNotExist:
#     #     return Response(
#     #         {"message": "This product does not exist"}, status=status.HTTP_404_NOT_FOUND
#     #     )

#     product = get_object_or_404(Product, pk=id)
#     product_dict = {"id": product.id, "name": product.name, "price": product.price}
#     return Response(product_dict)


@api_view()
def view_specific_product(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def view_categories(request):
    return Response({"message": "hello from category"})

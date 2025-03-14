from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category
from rest_framework import status
from product.serializers import ProductModelSerializer, CategoryModelSerializer
from django.db.models import Count

# Create your views here.
# def view_product(request):
#     return HttpResponse("Ok")


@api_view(["GET", "POST"])
def view_products(request):
    # products = Product.objects.select_related("category").all()
    # serializer = ProductModelSerializer(
    #     products, many=True, context={"request": request}
    # )
    # return Response(serializer.data)

    if request.method == "GET":
        products = Product.objects.select_related("category").all()
        serializer = ProductModelSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)
    if request.method == "POST":
        serializer = ProductModelSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["GET", "PUT", "DELETE"])
def view_specific_product(request, pk):
    if request.method == "GET":
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(product, context={"request": request})
        return Response(serializer.data)
    if request.method == "PUT":
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(
            product, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == "DELETE":
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def view_categories(request):
    # categories = Category.objects.annotate(product_count=Count("products")).all()
    # serializer = CategoryModelSerializer(categories, many=True)
    # return Response(serializer.data)

    if request.method == "GET":
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = CategoryModelSerializer(data=request.data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """ another way """
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategoryModelSerializer(category)
    return Response(serializer.data)

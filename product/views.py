from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category, Review, ProductImage
from rest_framework import status
from product.serializers import (
    ProductModelSerializer,
    CategoryModelSerializer,
    ReviewModelSerializer,
    ProductImageSerializer,
)
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import CustomProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from product.paginations import DefaultPagination

# from rest_framework.permissions import IsAdminUser, AllowAny
from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermission
from rest_framework.permissions import (
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
)
from product.permissions import IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
# def view_product(request):
#     return HttpResponse("Ok")


# FUNCTIONAL BASED VIEW:
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


# CLASS BASD VIEW
class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializer = ProductModelSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductModelSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# VIEW USING REST FRAMEWORK GENERIC VIEWS:
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductModelSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related("category").all()

    # def get_serializer_class(self):
    #     return ProductModelSerializer

    # def get_serializer_context(self):
    #     return {"request": self.request}


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


""" VIEWSET """


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
     - Allows authenticated admin to create, update and delete product
     - Allows users to browse and filter products
     - Support searching by name, description and category
     - Support ordering by price and updated_at
    """

    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["category_id", "price"]
    pagination_class = DefaultPagination
    filterset_class = CustomProductFilter
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["price", "updated_at"]
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [FullDjangoModelPermission]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAdminUser()]

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get("category_id")

    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id=category_id)

    #     return queryset

    @swagger_auto_schema(operation_summary="Retrieve a list of products")
    def list(self, request, *args, **kwargs):
        """Retrieve all products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow an admin to create a product",
        request_body=ProductModelSerializer,
        responses={201: ProductModelSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock < 10:
            return Response(
                {"message": "product stock more than 10 could not be deleted"}
            )
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


# FUNCATIONAL BASED VIEW
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


# CLASS BASED VIEW
class ViewSpecificProducts(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(product, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(
            product, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        # product = get_object_or_404(Product, pk=pk)
        # product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

        """TO SHOW THE DATA AFTER DELETING"""
        product = get_object_or_404(Product, pk=pk)
        copy_of_product = product
        product.delete()
        serializer = ProductModelSerializer(
            copy_of_product, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


# VIEW USING REST FRAMEWORK GENERIC VIEWS:
class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

    # lookup_url = "id"

    """ CUSTOMIZING GENERIC VIEW """

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.stock < 10:
            return Response(
                {"message": "product stock less than 10 could not be deleted"}
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# FUNCATIONAL BASED VIEW
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


# CLASS BASED VIEW
class ViewCategories(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# VIEW USING REST FRAMEWORK GENERIC VIEW:
class CategoryList(ListCreateAPIView):
    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("products")).all()

    def get_serializer_class(self):
        return CategoryModelSerializer


# FUNCTIONAL BASED VIEW
@api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategoryModelSerializer(category)
    return Response(serializer.data)


# CLASS BASED VIEW
class ViewSpecificCategory(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryModelSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# VIEW USING REST FRAMEWORK GENERIC VIEW:
class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


""" MODEL VIEW SETS """


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get("product_pk"))

    def get_serializer_context(self):
        return {"product_id": self.kwargs.get("product_pk")}


""" PRODUCT IMAGE VIEW SET """


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get("product_pk"))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get("product_pk"))

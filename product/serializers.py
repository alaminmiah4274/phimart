from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product


# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     description = serializers.CharField()


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    """ not optimize process """
    # product_count = serializers.SerializerMethodField(method_name="")

    # def get_product_count(self, category):
    #     count = Product.objects.filter(category=category).count()
    #     return count

    product_count = serializers.IntegerField(read_only=True)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     # price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     unit_price = serializers.DecimalField(
#         max_digits=10, decimal_places=2, source="price"
#     )

#     price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

#     # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     # category = serializers.StringRelatedField()
#     # category = CategorySerializer()
#     category = serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(), view_name="view-specific-category"
#     )

#     def calculate_tax(self, product):
#         return round(product.price * Decimal(1.1), 2)


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "price_with_tax",
        ]

    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(), view_name="view-specific-category"
    )

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)

    # field validation
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price could not be negative")
        return price

    # object validation:
    # def validation(self, field_name):
    #     if field_name["password1"] != field_name["password2"]:
    #         raise serializers.ValidationError("password did not match")
    #     return field_name

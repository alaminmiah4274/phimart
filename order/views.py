from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from order.models import Cart, CartItem, Order, OrderItem
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from order import serializers
from rest_framework import status


""" CART VIEWSET """


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    # queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]

    # admin cart_id = 548e31a4-e946-43d1-b964-80d875d2658c
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()

        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    # serializer_class = CartItemSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.AddCartItemSerializer
        elif self.request.method == "PATCH":
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, "swagger_fake_view", False):
            return context

        return {"cart_id": self.kwargs.get("cart_pk")}

    def get_queryset(self):
        return CartItem.objects.select_related("product").filter(
            cart_id=self.kwargs.get("cart_pk")
        )


""" ORDER VIEWSET """


class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "delete", "patch"]

    def get_permissions(self):
        if self.action in ["update_status", "destroy"]:
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(user=request.user, order=order)
        return Response({"status": "Order cancelled successfully"})

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = serializers.UpdateOrderSerializer(
            order, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": f"Order status updated to {request.data['status']}"})

    def get_serializer_class(self):
        if self.action == "cancel":
            return serializers.EmptySerializer
        if self.action == "create":
            return serializers.CreateOrderSerializer
        if self.action == "update_status":
            return serializers.UpdateOrderSerializer
        return serializers.OrderSerializer

    def get_serializer_context(self):
        if getattr(self, "swagger_fake_view", False):
            return super().get_serializer_context()
        return {"user_id": self.request.user.id, "user": self.request.user}

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()
        if self.request.user.is_superuser:
            return Order.objects.prefetch_related("items__product").all()
        return Order.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

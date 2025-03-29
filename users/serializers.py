from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "address",
            "phone_number",
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone_number",
        ]


""" 
USER ENDPOINTS:-->
user registration: auth/users
user login: auth/jwt/create
current user: auth/users/me
"""

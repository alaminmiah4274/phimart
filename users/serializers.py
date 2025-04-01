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
        ref_name = "CustomUser"
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

""" 
Interview: TCS Python Interview By TCS Team 2024 ! Real Live Recording ! TCS NQT and Ninja Hiring --> 
1. How do we write a program in python? What are the basic things we need to take care of?
2. What is suit in python?
3. What are the different types of data types in python?
4. What are the different ways to concatenate to tuple?
5. What is slice operator?
6. What are the different types of functions that we have in python?
7. Can you define a class in python? How will you write a code and it’s method for an Employee class?
Create a method to print and call an object for this class.
8. What is init and self keywords in python?
9. What is pass statement?
10. How can you get a first digit of a string?
11. Regular expressions?
12. Which class do we use for ‘regular expression’ in python?


Edit 1: what I was also asked.
1. What is the difference between modules and packages?
2. What is lambda function? Write its syntax/ expression in the chat box.
3. What is init? And what is self?

"""

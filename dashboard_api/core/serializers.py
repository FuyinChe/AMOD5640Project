# serialization for user creation

from django.contrib.auth.models import User

from rest_framework import serializers

#use mysql customer for test
from .models import Customer


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password']

        )

        return user

#build a serializer for customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
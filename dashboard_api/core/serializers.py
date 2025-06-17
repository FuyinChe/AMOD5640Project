# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer
from .models import EnvironmentalData


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data.get('username') or email.split('@')[0]
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )
        # Create Customer profile linked to this user
        customer = Customer.objects.create(user=user)
        customer.set_verification_code()

        return user




class EnvironmentalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalData
        fields = '__all__'
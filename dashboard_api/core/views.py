from datetime import datetime, timedelta
import random

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .permissions import IsAdmin
from .models import Customer

from django.contrib.auth.hashers import make_password


#import environmental data model and serializer
from rest_framework import generics
from .models import EnvironmentalData
from .serializers import EnvironmentalDataSerializer

class VerifyEmailView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
            customer = user.customer
        except User.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.verification_code != code:
            return Response({'error': 'Incorrect verification code'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.code_expires_at and datetime.now() > customer.code_expires_at:
            return Response({'error': 'Verification code expired'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        customer.email_verified = True
        customer.verification_code = None
        customer.code_expires_at = None
        customer.save()

        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

class UserRegisterView(APIView):
    permission_classes = []  # allow unauthenticated registration

    def post(self, request):
        data = request.data

        # Validate email domain
        email = data.get('email')
        if not email or not email.endswith('@trentu.ca'):
            return Response({'error': 'Only @trentu.ca emails are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password
        password = data.get('password')
        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if User with email exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create inactive User with hashed password
        username = email.split('@')[0]
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        # Generate verification code & expiry
        verification_code = str(random.randint(100000, 999999))
        code_expires_at = datetime.now() + timedelta(minutes=10)

        # Create related Customer profile
        Customer.objects.create(
            user=user,
            verification_code=verification_code,
            code_expires_at=code_expires_at,
            email_verified=False
        )

        # Here you can trigger sending email with verification_code if you want

        return Response({'message': 'User created successfully. Please verify your email.'}, status=status.HTTP_201_CREATED)


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({'message': 'Welcome, Admin!'})




class EnvironmentalDataList(generics.ListAPIView):
    queryset = EnvironmentalData.objects.all().order_by('-Year', '-Month', '-Day')[:100]#return 100
    serializer_class = EnvironmentalDataSerializer



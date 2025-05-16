from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from .serializers import UserCreateSerializer

from .permissions import IsAdmin

#import models
from .models import Customer
from .serializers import CustomerSerializer


class UserRegisterView(APIView):

    permission_classes = [] # allow unauthenticated registration

    def post(self,request):
        serializer = UserCreateSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User created succcessfully'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self,request):
        return Response({'message':'Welcome, Admin!'})

#import allow any
from rest_framework.permissions import AllowAny

class CustomerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # if it is authenticated, then response all data
        if request.user.is_authenticated:
            queryset = Customer.objects.all()
        # if it is not, then response 5 records
        else:
            queryset = Customer.objects.all()[:5]
        
        serializer = CustomerSerializer(queryset, many = True) 
        return Response(serializer.data)
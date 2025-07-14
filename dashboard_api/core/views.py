"""
Main views module - imports from decoupled modules
"""
# Import views from decoupled modules
from .auth_views import (
    VerifyEmailView,
    UserRegisterView,
    ResendVerificationCodeView,
    AdminDashboardView,
    UserInfoView
)

from .environmental_views import (
    EnvironmentalDataList,
    SampleEnvironmentalDataList,
    MonthlySummaryView
)

from .raw_data_views import (
    RawSnowDepthView,
    RawRainfallView,
    RawHumidityView,
    RawSoilTemperatureView,
    RawMultiMetricView
)

from .averaged_chart_views import (
    AveragedSnowDepthView,
    AveragedRainfallView,
    AveragedHumidityView,
    AveragedSoilTemperatureView,
    AveragedShortwaveRadiationView,
    AveragedWindSpeedView,
    AveragedAtmosphericPressureView,
    MultiMetricBoxplotView
)

from .email_views import (
    TestEmailView,
    TestMultipleEmailView
)

from django.conf import settings
from django.views.static import serve as static_serve
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

# Swagger documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AdminTestView(APIView):
    """
    Simple test endpoint to debug admin authentication.
    Accepts both JWT and session authentication.
    """
    permission_classes = [IsAdmin]
    authentication_classes = [SessionAuthentication]  # Allow session authentication

    @swagger_auto_schema(
        operation_description="Test admin authentication and permissions",
        responses={
            200: openapi.Response(
                description="Admin authentication successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_STRING),
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'is_authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'groups': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'permissions': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    }
                )
            ),
            403: 'Forbidden - Admin access required'
        }
    )
    def get(self, request):
        return Response({
            'message': 'Admin access confirmed!',
            'user': request.user.username,
            'user_id': request.user.id,
            'is_authenticated': request.user.is_authenticated,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'groups': list(request.user.groups.values_list('name', flat=True)),
            'permissions': list(request.user.get_all_permissions())
        })

# Re-export all views for backward compatibility
__all__ = [
    'VerifyEmailView',
    'UserRegisterView',
    'ResendVerificationCodeView',
    'AdminDashboardView',
    'UserInfoView',
    'EnvironmentalDataList',
    'SampleEnvironmentalDataList',
    'MonthlySummaryView',
    # Raw data views
    'RawSnowDepthView',
    'RawRainfallView',
    'RawHumidityView',
    'RawSoilTemperatureView',
    'RawMultiMetricView',
    # Averaged chart views
    'AveragedSnowDepthView',
    'AveragedRainfallView',
    'AveragedHumidityView',
    'AveragedSoilTemperatureView',
    'AveragedShortwaveRadiationView',
    'AveragedWindSpeedView',
    'AveragedAtmosphericPressureView',
    # Statistical chart views
    'MultiMetricBoxplotView',
    'TestEmailView',
    'TestMultipleEmailView',
    'AdminTestView'
] 
# core/urls.py
from django.urls import path, re_path
from .views import (
    AdminDashboardView, UserRegisterView, VerifyEmailView, EnvironmentalDataList,
    SampleEnvironmentalDataList, ResendVerificationCodeView, TestEmailView, 
    TestMultipleEmailView, UserInfoView, MonthlySummaryView,
    # Raw data views
    RawSnowDepthView, RawRainfallView, RawSoilTemperatureView, RawMultiMetricView,
    # Averaged chart views
    AveragedSnowDepthView, AveragedRainfallView, AveragedSoilTemperatureView,
)






urlpatterns = [path('admin-dashboard/', AdminDashboardView.as_view(),name='admin-dashboard'),
    # user register    
    path('register/', UserRegisterView.as_view(),name='user-register'),    
    #email verify
    path('verify/', VerifyEmailView.as_view(),name='verify-email'),    
    # resend verification code
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend-verification-code'),
    # test email configuration
    path('test-email/', TestEmailView.as_view(), name='test-email'),
    # test multiple email accounts
    path('test-multiple-email/', TestMultipleEmailView.as_view(), name='test-multiple-email'),
    path('environmental-data/', EnvironmentalDataList.as_view(), name='environmental-data'),
    path('sample/environmental-data/', SampleEnvironmentalDataList.as_view(), name='sample_environmental_data'),
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
    # monthly summary API
    path('monthly-summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    # Raw data APIs (with limits)
    path('raw/snow-depth/', RawSnowDepthView.as_view(), name='raw-snow-depth'),
    path('raw/rainfall/', RawRainfallView.as_view(), name='raw-rainfall'),
    path('raw/soil-temperature/', RawSoilTemperatureView.as_view(), name='raw-soil-temperature'),
    path('raw/multi-metric/', RawMultiMetricView.as_view(), name='raw-multi-metric'),
    
    # Averaged chart APIs (hourly, daily, monthly)
    path('charts/snow-depth/', AveragedSnowDepthView.as_view(), name='snow-depth-chart'),
    path('charts/rainfall/', AveragedRainfallView.as_view(), name='rainfall-chart'),
    path('charts/soil-temperature/', AveragedSoilTemperatureView.as_view(), name='soil-temperature-chart'),

]

# core/urls.py
from django.urls import path
from .views import AdminDashboardView, UserRegisterView, VerifyEmailView,EnvironmentalDataList,SampleEnvironmentalDataList, ResendVerificationCodeView, TestEmailView, TestMultipleEmailView, UserInfoView






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
]

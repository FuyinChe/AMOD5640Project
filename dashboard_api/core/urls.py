# core/urls.py
from django.urls import path
from .views import AdminDashboardView, UserRegisterView, VerifyEmailView,EnvironmentalDataList,SampleEnvironmentalDataList






urlpatterns = [path('admin-dashboard/', AdminDashboardView.as_view(),name='admin-dashboard'),
    # user register    
    path('register/', UserRegisterView.as_view(),name='user-register'),    
    #email verify
    path('verify/', VerifyEmailView.as_view(),name='verify-email'),    
    path('environmental-data/', EnvironmentalDataList.as_view(), name='environmental-data'),
    path('sample/environmental-data/', SampleEnvironmentalDataList.as_view(), name='sample_environmental_data'),
]

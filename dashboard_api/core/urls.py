# core/urls.py
from django.urls import path
from .views import AdminDashboardView, UserRegisterView, VerifyEmailView,EnvironmentalDataList






urlpatterns = [path('admin-dashboard/', AdminDashboardView.as_view(),name='admin-dashboard'),
    # user register    
    path('register/', UserRegisterView.as_view(),name='user-register'),    
    #email verify
    path('verify/', VerifyEmailView.as_view(),name='verify-email'),    
    path('environmental-data/', EnvironmentalDataList.as_view(), name='environmental-data'),

]

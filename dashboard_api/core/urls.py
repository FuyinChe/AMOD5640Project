# core/urls.py
from django.urls import path
from .views import AdminDashboardView, UserRegisterView, CustomerListView

urlpatterns = [
    path('admin-dashboard/', AdminDashboardView.as_view()),
    path('register/', UserRegisterView.as_view()),

    #add customers
    path('customers/', CustomerListView.as_view())
]

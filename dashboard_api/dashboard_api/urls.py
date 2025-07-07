"""
URL configuration for dashbord_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.http import JsonResponse

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
#test csrf exempt
from django.views.decorators.csrf import csrf_exempt

# Import the AdminDocsView from core
from core.views import AdminDocsView, AdminTestView

# Swagger/OpenAPI documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Dashboard API",
      default_version='v1',
      description="Environmental data API documentation",
      terms_of_service="https://www.trentfarmdata.org/terms/",
      contact=openapi.Contact(email="admin@trentfarmdata.org"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def root_view(request):
    return JsonResponse({"message": "Dashboard API is running."})

#test csrf exempt
# @csrf_exempt # type: ignore
# def test_cors(request):
#     return JsonResponse({'message': 'CORS test successful'})

handler404 = 'dashboard_api.views.custom_page_not_found_view'
handler500 = 'dashboard_api.views.custom_error_view'


urlpatterns = [
    path('', root_view),  # Root endpoint
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/token',TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Admin-only documentation
    path('api/docs/', AdminDocsView.as_view(), name='admin-docs'),
    path('api/docs/<str:path>/', AdminDocsView.as_view(), name='admin-docs-path'),
    # Admin test endpoint
    path('api/admin-test/', AdminTestView.as_view(), name='admin-test'),
    
    # Swagger/OpenAPI documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # path('test-cors/', test_cors),       # <-- add this for CORS testing
]

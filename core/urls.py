
from django.contrib import admin
from django.urls import path
from API import endpoints
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', endpoints.login,name='api-login'),
    path('api/auth/register/', endpoints.register_user,name='api-register'),
    path('api/auth/verify/', endpoints.verify_email,name='api-verify-email'),
]


from django.contrib import admin
from django.urls import path
from API import endpoints
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', endpoints.login,name='api-login'),
    path('api/auth/register/', endpoints.register_user,name='api-register'),
    path('api/auth/verify/', endpoints.verify_email,name='api-verify-email'),
    
    path('api/users/update/', endpoints.update_user,name='api-update-user'),
    path('api/users/delete/', endpoints.delete_user,name='api-delete-user'),

    path('api/sync/v1/',endpoints.sync_api_main_v1,name='sync-v1')
]

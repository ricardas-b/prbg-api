from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_app.urls')),
    path('api/v1/', include('quote_admin_app.urls')),
    
]
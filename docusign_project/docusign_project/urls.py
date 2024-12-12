
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls') ),
    path('', include('contracts.urls') ),
    path('api/', include('auth.urls')),
    # path('api/', include('auth.urls')),
]

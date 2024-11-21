from filebrowser.sites import site
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),       # Django admin
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth ilovasi
    path('', include('dashboard.urls')),  # Dashboard ilovasining URL-lari
    path('filemanager/', include('filemanager.urls')),
    path('logs/', include('logs.urls')),
    path('system_control/', include('system_control.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

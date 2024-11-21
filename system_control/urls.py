from django.urls import path
from .views import manage_service, check_service_status, manage_service_view, server_info, delete_log

urlpatterns = [
    path('manage/', manage_service, name='manage_service'),
    path('status/', check_service_status, name='check_service_status'),
    path('server-info/', server_info, name='server_info'),
    path('', manage_service_view, name='manage_service_view'),
    path('delete-log/<int:log_id>/', delete_log, name='delete_log'),
]

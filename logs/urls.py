from django.urls import path
from .views import get_logs, start_log_monitor, server_logs_view

urlpatterns = [
    path('', server_logs_view, name='server_logs'),  # HTML sahifa
    path('get-logs/', get_logs, name='get_logs'),    # Loglarni olish
    path('start-log-monitor/', start_log_monitor, name='start_log_monitor'),  # Log monitoringni boshlash
]

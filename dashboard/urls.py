from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('update/', views.update_project, name='update_project'),
    path('update-status/', views.get_update_status, name='get_update_status'),
    path('logout/', views.logout_view, name='logout'),
    path('get-logs/', views.get_logs, name='get_logs'),
]
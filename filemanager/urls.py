from django.urls import path
from .views import file_manager, delete_item, rename_item, copy_item, paste_item

urlpatterns = [
    path('', file_manager, name='file_manager'),
    path('delete/', delete_item, name='delete_item'),
    path('rename/', rename_item, name='rename_item'),
    path('copy/', copy_item, name='copy_item'),
    path('paste/', paste_item, name='paste_item'),
]

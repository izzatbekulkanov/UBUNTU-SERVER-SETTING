from django.contrib import admin
from .models import UpdateLog

@admin.register(UpdateLog)
class UpdateLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'status', 'progress')  # Admin panelda ko'rsatiladigan ustunlar
    list_filter = ('status',)  # Filtr qilish uchun ustunlar
    search_fields = ('status',)  # Qidiruv maydoni
    ordering = ('-timestamp',)  # Yozuvlarni tartiblash (so'nggi yozuv birinchi bo'lib chiqadi)

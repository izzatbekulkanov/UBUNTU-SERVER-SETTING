from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'log_type', 'message')
    list_filter = ('log_type', 'timestamp')
    search_fields = ('message',)

from django.db import models
from django.utils.timezone import now

class ServiceLog(models.Model):
    service_name = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    message = models.TextField()
    log_type = models.CharField(max_length=10, choices=[('INFO', 'Info'), ('ERROR', 'Error')])
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"[{self.timestamp}] {self.service_name} - {self.action.upper()}"

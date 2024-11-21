from django.db import models
from django.utils.timezone import now

class LogEntry(models.Model):
    timestamp = models.DateTimeField(default=now)
    log_type = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"[{self.timestamp}] {self.log_type}: {self.message}"

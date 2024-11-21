from django.db import models

class UpdateLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.timestamp} - {self.status} ({self.progress}%)"
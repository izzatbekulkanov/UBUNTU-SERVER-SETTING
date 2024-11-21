import subprocess
import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import LogEntry


# Asinxron loglarni olish uchun thread
def monitor_logs():
    try:
        process = subprocess.Popen(
            ['journalctl', '-u', 'inihub.service', '-f'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in iter(process.stdout.readline, ""):
            if line.strip():
                log_type = "error" if "ERROR" in line or "Fail" in line else "success"
                LogEntry.objects.create(log_type=log_type, message=line.strip())
    except Exception as e:
        LogEntry.objects.create(log_type="error", message=str(e))


# Loglarni olish uchun view
def get_logs(request):
    logs = LogEntry.objects.order_by('-timestamp')[:100]
    data = [{"timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "log_type": log.log_type, "message": log.message} for log in logs]
    return JsonResponse({"logs": data})


# Log monitoringni boshlash
@csrf_exempt
def start_log_monitor(request):
    if request.method == 'POST':
        threading.Thread(target=monitor_logs, daemon=True).start()
        return JsonResponse({"status": "Log monitoring started."})
    return JsonResponse({"error": "Invalid request method."}, status=400)


# HTML sahifani ko'rsatish uchun view
def server_logs_view(request):
    return render(request, 'logs/server_logs.html')

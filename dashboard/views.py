from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from .models import UpdateLog
import subprocess
import time
import threading  # threading modulini import qilish

@login_required
def home(request):
    """
    Asosiy sahifa loglari bilan birga qaytariladi.
    """
    logs = UpdateLog.objects.all().order_by('-timestamp')
    return render(request, 'home.html', {'logs': logs})


class UpdateThread(threading.Thread):
    """
    Yangilash jarayonini asinxron ravishda boshqaruvchi klass.
    """
    def __init__(self, log_id):
        super().__init__()
        self.log_id = log_id

    def run(self):
        log = UpdateLog.objects.get(id=self.log_id)
        try:
            log.status = "Updating..."
            log.save()

            # Deploy skriptni ishga tushirish
            process = subprocess.Popen(
                ['/home/superadmin/inihub/deploy.sh'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            progress = 0
            while process.poll() is None:
                time.sleep(1)
                progress += 20
                if progress > 100:
                    progress = 100
                log.status = f"Progress: {progress}%"
                log.progress = progress
                log.save()

            stdout, stderr = process.communicate()
            if process.returncode == 0:
                log.status = "Update Successful"
                log.progress = 100
            else:
                log.status = f"Update Failed: {stderr}"
                log.progress = 100
        except Exception as e:
            log.status = f"Error: {str(e)}"
            log.progress = 100
        finally:
            log.save()


@login_required
def update_project(request):
    """
    Yangilash jarayonini boshlash uchun view.
    """
    if request.method == 'POST':
        # Yangi log yaratish
        log = UpdateLog.objects.create(status="Starting Update...")

        # Asinxron jarayonni ishga tushirish
        thread = UpdateThread(log.id)
        thread.start()

        return JsonResponse({'progress': 0, 'status': log.status})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def get_update_status(request):
    """
    Yangilash jarayonining hozirgi holatini qaytarish.
    """
    if request.method == 'GET':
        try:
            log = UpdateLog.objects.latest('timestamp')
            progress = log.progress

            response_data = {
                'status': log.status,
                'progress': progress,
                'complete': progress >= 100
            }

            return JsonResponse(response_data)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'No updates yet', 'progress': 0, 'complete': False}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def get_logs(request):
    """
    Barcha loglarni JSON formatida qaytarish.
    """
    if request.method == 'GET':
        logs = UpdateLog.objects.all().order_by('-timestamp')
        log_list = [{
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'status': log.status,
            'progress': log.progress
        } for log in logs]

        return JsonResponse({'logs': log_list}, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def logout_view(request):
    """
    Foydalanuvchini tizimdan chiqaradi va login sahifasiga yo'naltiradi.
    """
    logout(request)
    return redirect('/accounts/login/')

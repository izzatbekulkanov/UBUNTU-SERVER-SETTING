from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ServiceLog
import subprocess
import json
import shutil
from django.shortcuts import get_object_or_404


@csrf_exempt
def manage_service(request):
    """
    Xizmatni boshqarish: start, restart, stop, enable.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            service_name = data.get('service_name', 'inihub.service')

            result = subprocess.check_output(
                ['sudo', 'systemctl', action, service_name],
                stderr=subprocess.STDOUT, text=True
            )
            save_log(service_name, action, result)
            return JsonResponse({'status': 'success', 'message': result})
        except subprocess.CalledProcessError as e:
            save_log(service_name, action, e.output, error=True)
            return JsonResponse({'status': 'error', 'message': e.output}, status=400)
        except Exception as e:
            save_log(service_name, action, str(e), error=True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def check_service_status(request):
    """
    Xizmat holatini tekshirish.
    """
    service_name = request.GET.get('service_name', 'inihub.service')
    try:
        result = subprocess.check_output(
            ['sudo', 'systemctl', 'is-active', service_name],
            stderr=subprocess.STDOUT, text=True
        )
        is_active = result.strip() == 'active'
        return JsonResponse({'status': 'success', 'active': is_active, 'message': result})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 'message': e.output}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def server_info(request):
    """
    Server haqida ma'lumot.
    """
    try:
        disk_usage = shutil.disk_usage("/")
        total_space = disk_usage.total // (1024 ** 3)
        used_space = disk_usage.used // (1024 ** 3)
        free_space = disk_usage.free // (1024 ** 3)

        # Portlar haqida ma'lumot
        try:
            open_ports = subprocess.check_output(['sudo', 'netstat', '-tuln'], stderr=subprocess.STDOUT, text=True)
        except FileNotFoundError:
            open_ports = subprocess.check_output(['sudo', 'ss', '-tuln'], stderr=subprocess.STDOUT, text=True)

        return JsonResponse({
            'status': 'success',
            'disk': {
                'total': f"{total_space} GB",
                'used': f"{used_space} GB",
                'free': f"{free_space} GB"
            },
            'ports': open_ports
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


import subprocess
import shutil
from django.shortcuts import render
from .models import ServiceLog

def manage_service_view(request):
    """
    HTML sahifani ko‘rsatish.
    """
    logs = ServiceLog.objects.all().order_by('-timestamp')[:50]

    # Disk va xotira ma'lumotlari
    disk_usage = shutil.disk_usage("/")
    total_space = disk_usage.total // (1024 ** 3)
    used_space = disk_usage.used // (1024 ** 3)
    free_space = disk_usage.free // (1024 ** 3)

    memory_info = subprocess.check_output(['free', '-h'], text=True)
    memory_info_lines = memory_info.strip().split("\n")
    memory_data = memory_info_lines[1].split()

    memory_total = memory_data[1]
    memory_used = memory_data[2]
    memory_free = memory_data[3]

    # Port ma'lumotlari
    try:
        port_data = subprocess.check_output(['sudo', 'netstat', '-tuln'], text=True)
    except FileNotFoundError:
        port_data = subprocess.check_output(['sudo', 'ss', '-tuln'], text=True)

    ports = {
        'open': [],
        'closed': []
    }

    port_risks = {
        "22": "SSH porti, agar parol kuchsiz bo'lsa, brute-force hujumlar xavfi mavjud.",
        "80": "HTTP porti, xavfsiz emas; TLS (HTTPS) orqali himoya tavsiya etiladi.",
        "443": "HTTPS porti, odatda xavfsiz, lekin eski sertifikatlar muammolarga olib kelishi mumkin.",
        "3306": "MySQL porti, tashqi kirish ochiq bo'lsa, ma'lumotlar o'g'irlanishi xavfi mavjud.",
        "5000": "Development porti, ishlab chiqarishda foydalanmaslik tavsiya etiladi.",
        "8000": "Django test server porti, ishlab chiqarishda foydalanmaslik kerak.",
        "8118": "Proxy server porti, to'g'ri sozlanmasa xavfsizlik teshigi bo'lishi mumkin."
    }

    for line in port_data.strip().split("\n"):
        if 'LISTEN' in line:
            port_info = line.strip()
            port_number = port_info.split()[3].split(":")[-1]
            risk = port_risks.get(port_number, "Ushbu port uchun xavfsizlik tavsiyasi mavjud emas.")
            ports['open'].append({"info": port_info, "risk": risk})
        else:
            ports['closed'].append(line.strip())

    return render(request, 'system_control/manage_service.html', {
        'logs': logs,
        'disk': {'total': total_space, 'used': used_space, 'free': free_space},
        'memory': {'total': memory_total, 'used': memory_used, 'free': memory_free},
        'ports': ports
    })


def save_log(service_name, action, message, error=False):
    """
    Loglarni saqlash uchun yordamchi funksiya.
    """
    log_type = "ERROR" if error else "INFO"
    ServiceLog.objects.create(
        service_name=service_name,
        action=action,
        message=message,
        log_type=log_type
    )


def delete_log(request, log_id):
    """
    Logni o'chirish funksiyasi.
    """
    if request.method == 'DELETE':
        try:
            log = get_object_or_404(ServiceLog, id=log_id)
            log.delete()
            return JsonResponse({'status': 'success', 'message': 'Log muvaffaqiyatli o‘chirildi.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Logni o‘chirishda xatolik yuz berdi: {str(e)}'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Noto‘g‘ri so‘rov usuli.'}, status=400)
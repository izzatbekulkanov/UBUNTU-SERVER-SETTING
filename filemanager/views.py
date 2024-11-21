import os
import shutil
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = "/home/superadmin/inihub"

def file_manager(request):
    """
    Fayllar va papkalarni boshqarish uchun view.
    """
    directory = request.GET.get("directory", BASE_DIR)
    parent_directory = os.path.dirname(directory)
    try:
        items = os.listdir(directory)
        folders = [f for f in items if os.path.isdir(os.path.join(directory, f))]
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        folders.sort()
        files.sort()

        folder_data = [{"name": f, "is_dir": True, "size": "-"} for f in folders]
        file_data = [{"name": f, "is_dir": False, "size": os.path.getsize(os.path.join(directory, f)) // 1024} for f in files]

        return render(
            request, "file_manager.html", {
                "directory": directory,
                "parent_directory": parent_directory,
                "files": folder_data + file_data,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_item(request):
    """
    Fayl yoki papkani o'chirish uchun view.
    """
    if request.method == "POST":
        directory = request.POST.get("directory", BASE_DIR)
        item_name = request.POST.get("name", "")
        item_path = os.path.join(directory, item_name)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            return JsonResponse({"message": f"'{item_name}' muvaffaqiyatli o'chirildi!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def rename_item(request):
    """
    Fayl yoki papka nomini o'zgartirish uchun view.
    """
    if request.method == "POST":
        directory = request.POST.get("directory", BASE_DIR)
        old_name = request.POST.get("old_name", "")
        new_name = request.POST.get("new_name", "")
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        try:
            os.rename(old_path, new_path)
            return JsonResponse({"message": f"'{old_name}' muvaffaqiyatli '{new_name}'ga o'zgartirildi!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def copy_item(request):
    """
    Fayl yoki papkani nusxalash uchun view.
    """
    if request.method == "POST":
        directory = request.POST.get("directory", BASE_DIR)
        item_name = request.POST.get("name", "")
        item_path = os.path.join(directory, item_name)
        copy_path = os.path.join(directory, f"{item_name}_copy")
        try:
            if os.path.isdir(item_path):
                shutil.copytree(item_path, copy_path)
            else:
                shutil.copy(item_path, copy_path)
            return JsonResponse({"message": f"'{item_name}' muvaffaqiyatli nusxalandi!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def paste_item(request):
    """
    Nusxalangan faylni joyiga qo'yish uchun view.
    """
    if request.method == "POST":
        source_path = request.POST.get("source_path", "")
        target_directory = request.POST.get("directory", BASE_DIR)
        try:
            shutil.copy(source_path, target_directory)
            return JsonResponse({"message": "Fayl muvaffaqiyatli joylashtirildi!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

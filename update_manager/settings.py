
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bt1m@*t&diu3ygu6j3oqv&zwsi476!ut8j+7%z8=-79r2gcv^3'

CSRF_TRUSTED_ORIGINS = [
    "https://updatehub.namspi.uz",
    "http://127.0.0.1:8118",  # Localhost uchun (zaruratga qarab)
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'filebrowser',
    'django.contrib.staticfiles',
    'dashboard',  # Dashboard ilovasi
    'filemanager',
    'logs',
    'system_control',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'update_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'dashboard' / 'templates'],  # Templates papkasiga yo'l
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'update_manager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'


USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / '/static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

import os

# Media va Static sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



LOGIN_URL = '/accounts/login/'  # Login URL
LOGIN_REDIRECT_URL = '/'        # Login qilgandan keyin asosiy sahifaga qaytish
LOGOUT_REDIRECT_URL = '/accounts/login/'  # Logoutdan keyin login sahifaga qaytish
"""
Django settings for todo project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import mimetypes
import os
from pathlib import Path
from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@&ivg06$5v6#yo+^*y9ixt^^a(7bncddv$p2p7k2d#+@iaoc)i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("IS_DEVELOPMENT", True)
#DEBUG = True
#ALLOWED_HOSTS = ['127.0.0.1', '192.168.100.100', 'localhost', '192.168.100.24', '192.168.18.191', 'vtodo.pl', 'vitodo.pl', 'h22.seohost.pl']
#ALLOWED_HOSTS = getenv("APP_HOST")
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
    'users.apps.UsersConfig',
    'crispy_forms',
    'calendar_app',
    'geolocation',
    'bootstrap4',
    'bootstrap_modal_forms',
    'bootstrap_datepicker_plus',
    'avatar',
    'pwa',
    'webpush',
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

BOOTSTRAP4 = {
    'include_jquery': True,
}

ROOT_URLCONF = 'todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'todo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3")),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

   # {
   #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
   # },

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
   # {
   #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
   # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pl-pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')
STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')
MEDIA_URL = '/media/'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = 'vtodo'
LOGIN_URL = 'index'
DATE_FORMAT = "d-m-Y"
DATE_INPUT_FORMATS = ['%d-%m-%Y']
TIME_FORMATS = ['%H:%M:%S']
mimetypes.add_type('image/svg+xml', '.svg', True)
#TIME_INPUT_FORMATS = '%H:%M'

STATICFILE_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": """BBhw6SWqTPBLfnLuRZIOt-3KKOabs3zLbuwKXlIpK-pf1FYD22-dClSsCfx9GcfseNM-GUVHh07FoE_Mhkd4FAQ""",
    "VAPID_PRIVATE_KEY": """mjynE_5IT9Olr__itIlY8gENcRe6MhZQI76XwhG5Vr4""",
    "VAPID_ADMIN_EMAIL": "adrcha2@st.amu.edu.pl"
}

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'templates', 'serviceworker.js')

PWA_APP_NAME = 'vTo-Do'
PWA_APP_DESCRIPTION = "Description"
PWA_APP_THEME_COLOR = '#A300C4'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [

    {
        'src': '/static/image/icon-192.png',
        'sizes': '192x192'
    }

]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/image/favicon.png',
        'sizes': '192x192'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/image/app-icon.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'pl-PL'
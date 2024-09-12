"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os, environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env() 


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
PROD = env('PROD')
if PROD == True:
    DEBUG=env('DEBUG_PROD')
else:
    DEBUG=env('DEBUG')
    

ALLOWED_HOSTS = env('ALLOW_HOSTS', default='').split(',') if env('ALLOW_HOSTS', default='') else []

AUTH_USER_MODEL = 'accounts.MUsua'
API_USR_TRACCAR = 'ierrakato98@gmail.com'
API_PSS_TRACCAR = '159357852Aj.'
API_USRID_TRACCAR = '17648'
API_KEY_SSMC = 'Bearer RjBEAiAacXPFcldc_mEzCMw2iFs7VvxBw1ta59jm34FgCuQ7FAIgV6WF5N_Cjg49lCfhkFXFqkt7P3e-lcS_M7i_KDS3yHJ7InUiOjE3NjQ4LCJlIjoiMjAyNS0wNy0yOFQwNTowMDowMC4wMDArMDA6MDAifQ'
API_TOKEN = 'RjBEAiAacXPFcldc_mEzCMw2iFs7VvxBw1ta59jm34FgCuQ7FAIgV6WF5N_Cjg49lCfhkFXFqkt7P3e-lcS_M7i_KDS3yHJ7InUiOjE3NjQ4LCJlIjoiMjAyNS0wNy0yOFQwNTowMDowMC4wMDArMDA6MDAifQ'
#produccion
# API_URL_BASE = 'https://ssmc.munimaynas.gob.pe'
# TRACCAR_URL_BASE = ''

#desarrollo
API_URL_BASE = 'https://neto.munimaynas.gob.pe'
TRACCAR_URL_BASE = 'https://demo2.traccar.org'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'dashboard',
    'gps_tracking',
    'tailwind',
    'theme',
    'django_browser_reload',
    'rest_framework',
    'websockets',
    'geopy',
]

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE_PROD'),
        'NAME': env('DB_NAME_PROD'),
        'USER': env('DB_USER_PROD'),
        'PASSWORD': env('DB_PASSWORD_PROD'),
        'HOST': env('DB_HOST_PROD'),
        'PORT': env('DB_PORT_PROD'),
        'OPTIONS': {'sql_mode': 'STRICT_ALL_TABLES'},
    },
    'local': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {'sql_mode': 'STRICT_ALL_TABLES'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    'accounts.backends.MUsuaBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
#local
#Produccion
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = "/home/munimaynas/neto.munimaynas.gob.pe/static"
MEDIA_ROOT = "/home/munimaynas/neto.munimaynas.gob.pe/media"

#Produccion
# STATIC_URL = 'static/'
# MEDIA_URL = "media/"

# STATIC_ROOT = "/home/munimaynas/ssmc.munimaynas.gob.pe/static"
# MEDIA_ROOT = "/home/munimaynas/ssmc.munimaynas.gob.pe/media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

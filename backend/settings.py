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


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
PROD = env('PROD')
if PROD == 'True':
    DEBUG=env('DEBUG_PROD')
    ALLOWED_HOSTS = env('ALLOW_HOSTS', default='').split(',') if env('ALLOW_HOSTS', default='') else []
    ALLOW_CORS = env('ALLOW_CORS', default='')
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in ALLOW_CORS.split(',') if origin.strip().startswith(('http://', 'https://'))]
else:
    DEBUG=env('DEBUG')
    ALLOWED_HOSTS = env('ALLOW_HOSTS_LOCAL', default='').split(',') if env('ALLOW_HOSTS_LOCAL', default='') else []
    ALLOW_CORS = env('ALLOW_CORS_LOCAL', default='')
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in ALLOW_CORS.split(',') if origin.strip().startswith(('http://', 'https://'))]
    

AUTH_USER_MODEL = 'accounts.MUsua'
API_USR_TRACCAR = 'ierrakato98@gmail.com'
API_PSS_TRACCAR = '159357852Aj.'
API_USRID_TRACCAR = '17648'
API_KEY_SSMC = 'Bearer RzBFAiEAqlQch7fRc34OaWG6FTOilAt1j2Ns_6RqXrnWC6F6k_8CICQjuQ5_kMwfOZYMsy_sfKM4Yb7UAXJCwxpVTPrEb27weyJ1Ijo0MTg0LCJlIjoiMjAyOC0xMi0xMFQwNTowMDowMC4wMDArMDA6MDAifQ'
API_TOKEN = 'RzBFAiEAqlQch7fRc34OaWG6FTOilAt1j2Ns_6RqXrnWC6F6k_8CICQjuQ5_kMwfOZYMsy_sfKM4Yb7UAXJCwxpVTPrEb27weyJ1Ijo0MTg0LCJlIjoiMjAyOC0xMi0xMFQwNTowMDowMC4wMDArMDA6MDAifQ'

#desarrollo
BUILD = env('BUILD')
if BUILD == 'True':
    API_URL_BASE = env('API_URL_BASE')
else:
    API_URL_BASE = env('API_URL_BASE_LOCAL')
    
TRACCAR_URL_BASE = env('TRACCAR_URL_BASE')
# Application definition

# print(ALLOWED_HOSTS)

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


DATABASES = {
    # 'default': {
    #     'ENGINE': env('DB_ENGINE_PROD'),
    #     'NAME': env('DB_NAME_PROD'),
    #     'USER': env('DB_USER_PROD'),
    #     'PASSWORD': env('DB_PASSWORD_PROD'),
    #     'HOST': env('DB_HOST_PROD'),
    #     'PORT': env('DB_PORT_PROD'),
    #     'OPTIONS': {'sql_mode': 'STRICT_ALL_TABLES'},
    # },
    'default': {
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
    "sesame.backends.ModelBackend",
]
SESAME_MAX_AGE = 12

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

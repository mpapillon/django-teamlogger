"""
Django settings for TeamLogger project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

def get_or_create_secret_key():
	"""
	Get the secret from environement varaibles or create it if not exists.
	"""
	import random
	import string
	
	secret_key = "".join( [random.choice(string.printable) for i in range(60)] )
	return os.getenv('APP_SECRET', secret_key)
	

SECRET_KEY = get_or_create_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'nouvelles.apps.NouvellesConfig',
    'markdown_deux',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'teamlogger.urls'

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

WSGI_APPLICATION = 'teamlogger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

def get_database_settings():
    """
    Get database settings from environement varaibles or returns defaults.
    """
    db_engines = {
        'sqlite': 'django.db.backends.sqlite3', 
        'postgres': 'django.db.backends.postgresql', 
        'mysql': 'django.db.backends.mysql', 
        'oracle': 'django.db.backends.oracle'
    }
    
    def create_sqlite_settings(path):
        return {
            'default': {
                'ENGINE': db_engines['sqlite'],
                'NAME': path,
            }
        }
    
    def create_database_settings(engine, name, host, port, user, passw):
        return {
            'default': {
                'ENGINE': db_engines[engine],
                'NAME': name,
                'HOST': host,
                'PORT': port,
                'USER': user,
                'PASSWORD': passw
            }
        }
    
    db_engine = os.getenv('DB_ENGINE', 'sqlite').lower()
    db_path = os.getenv('DB_PATH', '/home/docker/persistent/databases/teamlogger.db')
    
    # No DB_ENGINE, use default sqlite
    if db_engine not in db_engines:
        return create_sqlite_settings(db_path)
    
    db_name = os.getenv('DB_NAME', 'teamlogger')
    db_host = os.getenv('DB_HOST', 'db')
    db_port = os.getenv('DB_PORT', '')
    db_user = os.getenv('DB_USER', '')
    db_passw = os.getenv('DB_PASSWORD', '')
    
    if db_engine == 'sqlite':
        return create_sqlite_settings(db_path)
    else:
        return create_database_settings(db_engine, db_name, db_host, db_port, 
                                        db_user, db_passw)    
    

DATABASES = get_database_settings()


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = "/home/docker/volatile/static/"


# Media files
# https://docs.djangoproject.com/en/1.11/topics/files/

MEDIA_URL = '/media/'

MEDIA_ROOT = "/home/docker/persistent/media/"


# Auth urls
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-url
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-redirect-url
# https://docs.djangoproject.com/en/1.11/ref/settings/#logout-redirect-url

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# Emails settings
# https://docs.djangoproject.com/en/1.11/topics/email/#smtp-backend

EMAIL_HOST = os.getenv('APP_EMAIL_HOST', 'localhost')

EMAIL_PORT = os.getenv('APP_EMAIL_PORT', 25)

EMAIL_HOST_USER = os.getenv('APP_EMAIL_HOST_USER', '')

EMAIL_HOST_PASSWORD = os.getenv('APP_EMAIL_HOST_PASSWORD', '')

EMAIL_USE_TLS = os.getenv('APP_EMAIL_USE_TLS', False)

EMAIL_USE_SSL = os.getenv('APP_EMAIL_USE_SSL', False)

EMAIL_TIMEOUT = os.getenv('APP_EMAIL_TIMEOUT', None)

EMAIL_SSL_KEYFILE = os.getenv('APP_EMAIL_SSL_KEYFILE', None)

EMAIL_SSL_CERTFILE = os.getenv('APP_EMAIL_SSL_CERTFILE', None)


# Markdown deux settings

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            "fenced-code-blocks": None,
            "tables": None
        },
        "safe_mode": "escape",
    },
}


# Nouvelles Settings

SITE_NAME = os.getenv('APP_SITE_NAME', "TeamLogger")

HEADLINES_DAYS = os.getenv('APP_SITE_HEADLINES_DAYS', 7)

EMAIL_HIGH_ARTICLES = os.getenv('APP_EMAIL_HIGH_ARTICLES', False)

SITE_URL = ""

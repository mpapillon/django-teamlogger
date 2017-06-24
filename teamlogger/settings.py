"""
Django settings for TeamLogger project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import environ


env = environ.Env(APP_DEBUG=(bool, False), APP_SITE_NAME=(str, 'TeamLogger'), APP_LOG_LEVEL=(str, 'ERROR'))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
root = environ.Path(__file__) - 2
public_root = root.path('public/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


def get_or_create_secret_key():
    """
    Get the secret from environement varaibles or create it if not exists.
    """
    import random
    import string

    # SECURITY WARNING: keep the secret key used in production secret!
    secret_key = "".join([random.choice(string.printable) for i in range(60)])
    return os.getenv('APP_SECRET', secret_key)


SECRET_KEY = get_or_create_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('APP_DEBUG')

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
    'django_python3_ldap',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

DATABASES = {
    'default': env.db(default='sqlite:///teamlogger.db'),
}


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# django-python3-ldap configuration
# https://github.com/etianen/django-python3-ldap

# The URL of the LDAP server.
LDAP_URL = env.str("LDAP_URL", "")  # "ldap://localhost:10389"

if LDAP_URL:
    # Turning on LDAP backend (Authentication backend)
    # https://docs.djangoproject.com/en/1.11/ref/settings/#authentication-backends

    AUTHENTICATION_BACKENDS = (
        'django_python3_ldap.auth.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    # User model fields mapped to the LDAP
    # attributes that represent them.
    LDAP_AUTH_USER_FIELDS = env.json("LDAP_AUTH_USER_FIELDS", {
        "username": "uid",
        "first_name": "cn",
        "last_name": "sn",
        "email": "mail"
    })


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

LANGUAGE_CODE = env.str('APP_LANGUAGE_CODE', 'en-us')

TIME_ZONE = env.str('APP_TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

try:
    STATIC_ROOT = env('APP_STATIC_ROOT')
except environ.ImproperlyConfigured:
    STATIC_ROOT = public_root('staticfiles')

STATIC_URL = '/static/'


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# Media files
# https://docs.djangoproject.com/en/1.11/topics/files/

try:
    MEDIA_ROOT = env('APP_MEDIA_ROOT')
except environ.ImproperlyConfigured:
    MEDIA_ROOT = public_root('mediafiles')

MEDIA_URL = '/media/'


# Auth urls
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-url
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-redirect-url
# https://docs.djangoproject.com/en/1.11/ref/settings/#logout-redirect-url

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# Emails settings
# https://docs.djangoproject.com/en/1.11/topics/email/#smtp-backend

EMAIL_CONFIG = env.email(default='dummymail://')
vars().update(EMAIL_CONFIG)


# Markdown deux settings

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "fenced-code-blocks": None,
            "tables": None,
            "header-ids": None,
        },
        "safe_mode": "escape",
    },
}


# Logging configuration, prints everything in console
# https://docs.djangoproject.com/en/1.11/topics/logging/#configuring-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('APP_LOG_LEVEL'),
        },
    },
}


# Nouvelles Settings

SITE_NAME = env('APP_SITE_NAME')

SITE_DOMAIN = env.str('APP_SITE_DOMAIN', '')

HEADLINES_DAYS = env.int('APP_SITE_HEADLINES_DAYS', 7)

EMAIL_HIGH_ARTICLES = env.bool('APP_EMAIL_HIGH_ARTICLES', False)

if EMAIL_HIGH_ARTICLES and not SITE_DOMAIN:
    raise environ.ImproperlyConfigured("You need a SITE_DOMAIN if you want email sending.")

LICENCE_FILE = root('LICENCE')

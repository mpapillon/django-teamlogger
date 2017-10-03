"""
Django settings for TeamLogger project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import environ


env = environ.Env(APP_DEBUG=(bool, False), APP_SITE_NAME=(str, 'TeamLogger'), APP_LOG_LEVEL=(str, 'ERROR'))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
root = environ.Path(__file__) - 3
public_root = root.path('public/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/



SECRET_KEY = env('APP_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('APP_DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'nouvelles.apps.NouvellesConfig',
    'ldapab.apps.LDAPAuthConfig',
    'spectre.apps.SpectreConfig',
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

DATABASES = {
    'default': env.db(default='sqlite:///teamlogger.db'),
}

# Turning on LDAP backend (Authentication backend)
# https://docs.djangoproject.com/en/1.11/ref/settings/#authentication-backends

AUTHENTICATION_BACKENDS = [
    'ldapab.auth.LDAPAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LDAP_SERVERS = {
    'default': {
        'ATTRIBUTES': {
            'username': ['uid', 'userid'],
            'email': ['mail', 'email'],
            'first_name': ['gn', 'cn'],
            'last_name':  'sn',
            'avatar': ['jpegPhoto', 'thumbnailPhoto'],
        }
    }
}


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



# Application context path
APP_CONTEXT = os.getenv('APP_CONTEXT', '/')
APP_CONTEXT = APP_CONTEXT if len(APP_CONTEXT) > 0 and APP_CONTEXT[-1] == '/' else '%s/' % APP_CONTEXT

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

try:
    STATIC_ROOT = env('APP_STATIC_ROOT')
except environ.ImproperlyConfigured:
    STATIC_ROOT = public_root('staticfiles')

STATIC_URL = '%sstatic/' % APP_CONTEXT


# Media files
# https://docs.djangoproject.com/en/1.11/topics/files/

try:
    MEDIA_ROOT = env('APP_MEDIA_ROOT')
except environ.ImproperlyConfigured:
    MEDIA_ROOT = public_root('mediafiles')

MEDIA_URL = '%smedia/' % APP_CONTEXT


# Auth urls
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-url
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-redirect-url
# https://docs.djangoproject.com/en/1.11/ref/settings/#logout-redirect-url

LOGIN_URL = '%slogin/' % APP_CONTEXT

LOGIN_REDIRECT_URL = APP_CONTEXT

LOGOUT_REDIRECT_URL = APP_CONTEXT


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


# Nouvelles Settings

SITE_NAME = env('APP_SITE_NAME')

SITE_DOMAIN = env.str('APP_SITE_DOMAIN', '')

HEADLINES_DAYS = env.int('APP_SITE_HEADLINES_DAYS', 7)

EMAIL_HIGH_ARTICLES = env.bool('APP_EMAIL_HIGH_ARTICLES', False)

if EMAIL_HIGH_ARTICLES and not SITE_DOMAIN:
    raise environ.ImproperlyConfigured("You need a SITE_DOMAIN if you want email sending.")

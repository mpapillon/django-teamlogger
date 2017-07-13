try:
    from teamlogger.settings import *
except ImportError:
    pass

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1']

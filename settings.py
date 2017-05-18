"""Contains Nouvelles settings"""
from django.conf import settings


def get(key, default):
    """
    Returns the value of key from global settings or the default value.
    """
    return getattr(settings, key, default)

# Number of days in headlines page
HEADLINES_DAYS = get('HEADLINES_DAYS', 7)

# Site footer
SITE_FOOTER = get('SITE_FOOTER', "A newspaper for your team")

# Site name
SITE_NAME = get('SITE_NAME', "Nouvelles")

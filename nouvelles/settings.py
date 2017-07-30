"""Contains Nouvelles settings"""
from os import path
from django.conf import settings


def get(key, default):
    """
    Returns the value of key from global settings or the default value.
    """
    return getattr(settings, key, default)

ACKNOWLEDGMENTS_FILE = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'ACKNOWLEDGMENTS.md')

# Number of days in headlines page
HEADLINES_DAYS = get('HEADLINES_DAYS', 7)

# Send or not an email when an article with HIGH criticality is posted.
EMAIL_HIGH_ARTICLES = get('EMAIL_HIGH_ARTICLES', False)

# Site name
SITE_NAME = get('SITE_NAME', "Nouvelles")

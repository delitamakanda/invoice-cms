"""
WSGI config for invoices project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

if settings.DEBUG:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoices.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoices.settings_prod')

application = get_wsgi_application()

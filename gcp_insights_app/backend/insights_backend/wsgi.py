"""
WSGI config for insights_backend project.

It exposes the WSGI callable as a module‑level variable named
``application``.  This file is used by Django's development server
and by WSGI servers such as gunicorn.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insights_backend.settings')

application = get_wsgi_application()

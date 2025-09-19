"""
Root URL configuration for the insights_backend project.

This file routes the top‑level URLs to the appropriate app.  The
`analytics` app provides API endpoints under `/api/`.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('analytics.urls')),
]

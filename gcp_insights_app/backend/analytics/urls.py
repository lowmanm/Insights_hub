"""
URL routes for the analytics app.

All endpoints are namespaced under `/api/` via the project’s root
`urls.py`.  You can add more endpoints here as your application grows.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('insights-summary/', views.insights_summary, name='insights-summary'),
    path('chat/', views.chat, name='chat'),
]

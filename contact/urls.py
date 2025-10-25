"""
File: urls.py
Author: Reagan Zierke
Date: 2025-10-25
Description: URL configurations for the contact app.
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.contact_view, name="contact"),
]

"""
File: urls.py
Author: Reagan Zierke
Date: 2025-10-25
Description: URL configurations for the home app.
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
]
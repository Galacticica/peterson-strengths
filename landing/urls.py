"""
File: urls.py
Author: Reagan Zierke
Date: 2025-11-05
Description: description
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
]
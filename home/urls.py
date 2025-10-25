"""
File: urls.py
Author: Reagan Zierke
Date: 2025-10-25
Description: description
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
]
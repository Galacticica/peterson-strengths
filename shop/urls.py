"""
File: urls.py
Author: Reagan Zierke
Date: 2025-10-27
Description: description
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
]
"""
File: views.py
Author: Reagan Zierke <reaganzierke@gmail.com>
Date: 2025-10-25
Description: Views for the home page.
"""


from django.shortcuts import render, redirect


def home_view(request):
    return render(request, 'home/home.html')

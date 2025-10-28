"""
File: views.py
Author: Reagan Zierke <reaganzierke@gmail.com>
Date: 2025-10-25
Description: Views for the home page.
"""


from django.shortcuts import render, redirect
from testimonials.models import Review


def home_view(request):
    top_reviews = Review.objects.all().order_by('-rating')[:3]
    return render(request, 'home/home.html', {'top_reviews': top_reviews})

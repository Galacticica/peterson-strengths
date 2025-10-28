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
    
    # Format author names to show only first letter of last name
    for review in top_reviews:
        parts = review.author.split()
        if len(parts) > 1:
            review.display_author = f"{' '.join(parts[:-1])} {parts[-1][0]}."
        else:
            review.display_author = review.author
    
    return render(request, 'home/home.html', {'top_reviews': top_reviews})

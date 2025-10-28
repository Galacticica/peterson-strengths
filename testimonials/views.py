from django.shortcuts import render
from .models import Review

def review_view(request):
    reviews = Review.objects.all().order_by('-rating')
    return render(request, 'testimonials/reviews.html', {'reviews': reviews})

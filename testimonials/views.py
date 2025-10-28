from django.shortcuts import render

def review_view(request):
    return render(request, 'testimonials/reviews.html')

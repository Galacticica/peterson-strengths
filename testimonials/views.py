from django.shortcuts import render
from .models import Review

def review_view(request):
    reviews = Review.objects.all().order_by('-rating')
    
    # Format author names to show only first letter of last name
    for review in reviews:
        parts = review.author.split()
        if len(parts) > 1:
            review.display_author = f"{' '.join(parts[:-1])} {parts[-1][0]}."
        else:
            review.display_author = review.author
    
    return render(request, 'testimonials/reviews.html', {'reviews': reviews})

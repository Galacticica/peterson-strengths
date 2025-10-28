from django.shortcuts import render
from .models import Product

def shop_view(request):
    products = Product.objects.all().order_by('price')
    return render(request, 'shop/shop.html', {'products': products})
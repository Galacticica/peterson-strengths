from django.shortcuts import render, get_object_or_404
from .models import Product

def shop_view(request):
    products = Product.objects.all().order_by('price')
    return render(request, 'shop/shop.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product.html', {'product': product})
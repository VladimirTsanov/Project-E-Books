from django.shortcuts import render
from .models import Product  # Импортираш модела

def home(request):
    products = Product.objects.all()  # Взема всички продукти от базата
    return render(request, 'index.html', {'products': products})
from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'home.html', {'products': products})

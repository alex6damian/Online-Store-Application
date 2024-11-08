from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the store index.")

def filtered_products(request):
    filtered_products = Product.objects.filter(category__name__exact='shoes')

    filtered_products = filtered_products.filter(price__gt=100, price__lt=800)
    return HttpResponse("You're looking at the filtered products.")

def products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'products':page_obj})
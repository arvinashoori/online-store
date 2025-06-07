from django.shortcuts import render
from .models import Category,Product
from django.shortcuts import get_object_or_404



def home(request , category_slug = None):
    products = None
    category_page = None

    if category_slug != None :
        category_page = get_object_or_404(Category , slug = category_slug)
        products = Product.objects.filter(category = category_page , available = True)
    else :    
        products = Product.objects.all().filter(available=True)


    return render(request,'core/home.html',{"category": category_page ,"products": products})


def product_page(request , category_slug , product_slug):

    try:
        product = Product.objects.get(slug = product_slug , category__slug = category_slug)
    except Exception as i : 
        raise i
    return render(request,'core/product.html',{"product": product})


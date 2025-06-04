from django.shortcuts import render
from .models import Category,Product



def home(request):
    products = Product.objects.all().filter(available=True)
    return render(request,'core/home.html',{"products": products})
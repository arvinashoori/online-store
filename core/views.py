from django.shortcuts import render,redirect
from .models import Category,Product,Cart,CartItem
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required,permission_required
from django.conf import settings


def home(request , category_slug = None):
    products = None
    category_page = None
    
    if category_slug != None :
        category_page = get_object_or_404(Category , slug = category_slug)
        products = Product.objects.filter(category = category_page , available = True)
   
    else :    
        products = Product.objects.all().filter(available=True)


    return render(request,'core/home.html',{"category": category_page ,"products": products })


def search_products(request):
    query = request.GET.get('q', '')   
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()  
    return render(request, 'core/search_results.html', {'products': products, 'query': query})


def product_page(request , category_slug , product_slug):

    try:
        product = Product.objects.get(slug = product_slug , category__slug = category_slug)
    except Exception as i : 
        raise i
    return render(request,'core/product.html',{"product": product})

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)

    try :
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product = product , cart = cart) 
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1 
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product = product ,
                                            cart = cart ,
                                            quantity = 1 ,
                                            )
        cart_item.save()

    return redirect('cart_detail')     

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart , active = True)
        

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
        cart_total = total   

    except Cart.DoesNotExist:
        cart_items = []
        cart_total = 0
        counter = 0

    return render(request, 'core/cart.html',dict(cart_items=cart_items,
                                                 total=total,
                                                 counter=counter,
                                                 cart_total=cart_total))

def cart_remove(request , product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product , id = product_id)
    cart_item = CartItem.objects.get(product=product , cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()
    return redirect('cart_detail')        

def cart_remove_product(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product , id = product_id)
    cart_item = CartItem.objects.get(product=product , cart=cart)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        total = sum(item.product.price * item.quantity for item in cart_items)
        counter = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        counter = 0
    return render(request, 'payments/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })



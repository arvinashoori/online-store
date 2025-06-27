import stripe 
from django.conf import settings 
from django.shortcuts import render, redirect 
from django.http import JsonResponse 
from core.models import Cart, CartItem ,Product
from .models import Order, OrderItem, Payment 
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required,permission_required

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@csrf_exempt
def create_checkout_session(request): 
    try: 
        cart = Cart.objects.get(cart_id=request.session.session_key) 
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                'currency': 'usd',
                'product_data': {
                        'name': item.product.name,
                                    },
                'unit_amount': int(item.product.price * 100),
                                 },
                'quantity': item.quantity,
        })

        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/payments/success/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
        metadata={'cart_id': cart.cart_id}
    )
        return JsonResponse({'id': session.id})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'سبد خرید یافت نشد'}, status=400)
    except Exception as e:
        print('Stripe error:', str(e))
        return JsonResponse({'error': str(e)}, status=400)

def success(request): 
    try: 
        cart = Cart.objects.get(cart_id=request.session.session_key) 
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        order_number = str(uuid.uuid4())[:8]   
        # جمع‌آوری اطلاعات کاربر (برای مثال، فرض می‌کنیم ایمیل و آدرس از فرم دریافت شده)
        email = request.user.email if request.user.is_authenticated else 'guest@example.com'
        address = 'آدرس نمونه'  # این باید از فرم دریافت شود        
        total = sum(item.product.price * item.quantity for item in cart_items)        
       
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=order_number,
            email=email,
            address=address,
            total=total
        )
    
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            products = Product.objects.get(id = item.product.id)
            products.stock = int(item.product.stock - item.quantity)
            products.save()
            item.delete()
    
        # دریافت اطلاعات پرداخت از Stripe (برای مثال، فرض می‌کنیم session_id از URL یا metadata در دسترس است)
        session_id = request.GET.get('session_id')  # در عمل باید از webhook استفاده شود
        payment = Payment.objects.create(
            order=order,
            stripe_payment_id=session_id or 'test_payment_id',
            amount=total
        )
        
        # خالی کردن سبد خرید
        cart.cartitem_set.all().delete()
    
    except Cart.DoesNotExist:
        pass

    return render(request, 'payments/success.html', {'order': order})


def cancel(request): 
    
    return render(request, 'payments/cancel.html')





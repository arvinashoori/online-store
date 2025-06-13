import stripe 
from django.conf import settings 
from django.shortcuts import render, redirect 
from django.http import JsonResponse 
from core.models import Cart, CartItem
from django.views.decorators.csrf import csrf_exempt



stripe.api_key = settings.STRIPE_SECRET_KEY

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
        )
        return JsonResponse({'id': session.id})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'سبد خرید یافت نشد'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def success(request):
    try:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart.cartitem_set.all().delete()
    except Cart.DoesNotExist:
        pass
    return render(request, 'payments/success.html')

def cancel(request):
    return render(request, 'payments/cancel.html')
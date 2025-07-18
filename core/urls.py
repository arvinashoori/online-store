from django.contrib import admin
from django.urls import path
from core import views



urlpatterns = [
    path('',views.home,name='home'),
    path('category/<slug:category_slug>',views.home,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',views.product_page,name='product_detail'),
    path('cart/',views.cart_detail , name="cart_detail"),
    path('cart/add/<int:product_id>',views.add_cart , name = 'add_cart'),
    path('cart/remove/<int:product_id>',views.cart_remove , name = 'cart_remove'),
    path('cart/remove_product/<int:product_id>',views.cart_remove_product , name = 'cart_remove_product'),
    path('checkout/',views.checkout , name = 'checkout'),
    path('search/', views.search_products, name='search_products'),



]

from django.db import models 
from core.models import Product
from django.contrib.auth.models import User

class Order(models.Model):

    STATUS_CHOICES = (('pending', 'Pending'),
                      ('processing', 'Processing'),
                      ('shipped', 'Shipped'),
                      ('delivered', 'Delivered'),
                      ('cancelled', 'Cancelled'),)
    phone_number = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    order_number = models.CharField(max_length=20, unique=True) 
    email = models.EmailField(max_length=100) 
    address = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending') 
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    quantity = models.IntegerField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class Payment(models.Model): 

    order = models.OneToOneField(Order, on_delete=models.CASCADE) 
    stripe_payment_id = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=20, default='completed') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.order_number}"
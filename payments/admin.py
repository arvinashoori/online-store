from django.contrib import admin 
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline): 
    model = OrderItem 
    extra = 0 
    readonly_fields = ('product', 'quantity', 'price') 
    can_delete = False

class OrderAdmin(admin.ModelAdmin): 
    list_display = ('order_number', 'user', 'email', 'total', 'status', 'created_at') 
    list_filter = ('status', 'created_at') 
    search_fields = ('order_number', 'email', 'user__username') 
    fieldsets = (

        ('Personal info', {
            'fields': ('email', 'address', 'user'),
            'classes': ('wide',)
        }),
        ('Important dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at','user','email','address') 
    inlines = [OrderItemInline]

class PaymentAdmin(admin.ModelAdmin): 
    list_display = ('order', 'stripe_payment_id', 'amount', 'status', 'created_at') 
    search_fields = ('order__order_number', 'stripe_payment_id')

admin.site.register(Order, OrderAdmin) 
admin.site.register(OrderItem) 
admin.site.register(Payment, PaymentAdmin)
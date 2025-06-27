from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin 
from .models import User 
from payments.models import Order

class OrderInline(admin.TabularInline): 
    model = Order 
    extra = 0 
    readonly_fields = ('order_number', 'email', 'address', 'total', 'status', 'created_at') 
    can_delete = False 
    show_change_link = True 

class CustomUserAdmin(UserAdmin): 
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'is_active') 
    list_filter = ('is_active', 'gender') 
    search_fields = ('username', 'email') 
    fieldsets = ( 
        (None, {
            'fields': ('username', 'password')
            }), ('Personal Info', {
                'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'age', 'gender', 'description')
                }), 
                ('Permissions', {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
                    }), ('Important dates', {
                        'fields': ('last_login', 'date_joined')
                        }), ) 
    filter_horizontal = ('groups', 'user_permissions') 
    readonly_fields = ('date_joined',) 
    inlines = [OrderInline]

admin.site.register(User, CustomUserAdmin)
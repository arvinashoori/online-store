from django.db import models 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 

    GENDER_CHOICES = (("M", "Male"), ("F", "Female")) 

    address = models.TextField(max_length=250, null=True, blank=True) 
    age = models.PositiveSmallIntegerField(null=True, blank=True) 
    description = models.TextField(max_length=250, null=True, blank=True) 
    email = models.EmailField(max_length=30, null=True, blank=True) 
    phone = models.CharField(max_length=15, null=True, blank=True)  
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=True, blank=True)
    first_name = models.CharField(max_length=30,null= True,blank=True)
    last_name = models.CharField(max_length=30,null= True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # رفع تداخل با related_name سفارشی
    
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
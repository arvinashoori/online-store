from django.urls import path
from . import views

urlpatterns =  [ path('create/', views.signupView, name='signup'), 
                path('signin/', views.signinView, name='signin'), 
                path('signout/', views.signuotView, name='signout'), ]
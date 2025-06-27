from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):


    class Meta:
        model = User
        fields = ['username','phone','first_name','last_name','email']
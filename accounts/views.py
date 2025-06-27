from django.shortcuts import render
from .forms import SignUpForm
from .models import User
from .models import  User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            signup_user = User.objects.get(username=username,
                                           phone=phone,email=email,
                                           last_name=last_name,first_name=first_name)
            #customer_group = Group.objects.get(name='Customers')
            #customer_group.user_set.add(signup_user)
            login(request, signup_user)
    else :
            form = SignUpForm()

    return render(request,'accounts/signup.html',{'form': form})    

def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                return redirect('signup')
    else:
            form = AuthenticationForm()

    return render(request,'accounts/signin.html',{'form': form})


@csrf_exempt
def signuotView(request):
    logout(request)
    return redirect('signin')



from django.shortcuts import redirect, render
from .models import Product
from .models import Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.db.models import Q


# Create your views here.
def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def home(request):
    products = Product.objects.all()[:4]
    return render(request,'home.html',{'products':products})

def categories(request):
    categorys= Category.objects.all();
    return render(request,'categories.html',{'categorys':categorys})

def categorypr(request,foo):
    #replace hyphen with spaces
    foo=foo.replace('-',' ')
    try:
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request,'categorypr.html',{'products':products,'category':category})
    except:
        messages.success(request,("No such category"))
        return redirect('categories')

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request,("Credential Error"))
            return redirect('login')

    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been Logged Out"))
    return redirect('home')

def register_user(request):
    form= SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            password=form.cleaned_data['password1']
            # loging in user
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have registered successfully"))
            return redirect('home')
        else:
            messages.success(request,(form.errors))
            print(form.errors)
            return redirect('register')

    else:
        return render(request,'register.html',{'form':form})
    

def searchproduct(request):
    query=request.GET.get('query')
    products=Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
    return render(request,'searchproduct.html',{'products':products,'query':query})

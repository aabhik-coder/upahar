from django.shortcuts import render
from .models import Product
from .models import Category
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def categories(request):
    categorys= Category.objects.all();
    return render(request,'categories.html',{'categorys':categorys})
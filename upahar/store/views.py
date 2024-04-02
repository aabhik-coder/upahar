from django.shortcuts import redirect, render
from .models import Product,Order
from .models import Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.db.models import Q
from .FinalTweetCategoryClassification import classifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .cossim import calc_cosine_similarity
from .tfidfvector import calculate_tf,calculate_tfidf,calculate_idf,tokenize
import numpy as np
from scipy.sparse import csr_matrix

# Create your views here.
def product(request,pk):
    # product = Product.objects.get(id=pk)
    # all_products = Product.objects.exclude(id=pk)
    # return render(request,'product.html',{'product':product,'relatedpr':all_products})

    chosen_product = Product.objects.get(id=pk)

    # Get all products excluding the chosen one
    all_products = Product.objects.exclude(id=pk)

    # Extract product descriptions
    product_descriptions = [chosen_product.name] + [product.name for product in all_products]


    idf = calculate_idf(product_descriptions)
    # Get sorted list of unique terms or voabulary
    unique_terms = sorted(set(term for doc in product_descriptions for term in tokenize(doc)))

    # Create a dictionary to map terms to their column indices
    term_to_index = {term: index for index, term in enumerate(unique_terms)}

    # Initialize lists to store row, column, and data values for CSR matrix
    rows = []
    cols = []
    data = []

    # Iterate through each document to populate the CSR matrix
    for document_index, document in enumerate(product_descriptions):
        tfidf_vector = calculate_tfidf(document, idf)
        for term, tfidf_value in tfidf_vector.items():
            term_index = term_to_index[term]
            rows.append(document_index)
            cols.append(term_index)
            data.append(tfidf_value)

    # Create the CSR matrix
    tfidf_csr_matrix = csr_matrix((data, (rows, cols)), shape=(len(product_descriptions), len(unique_terms)))
    print(tfidf_csr_matrix)
    cosine_similarities = calc_cosine_similarity(tfidf_csr_matrix[0], tfidf_csr_matrix[1:])
    print(cosine_similarities)

    # Get indices of the most similar products
    similar_products_indices = np.argsort(cosine_similarities)[::-1][:3]
    print(similar_products_indices)
    # Convert indices to integers
    similar_products_indices = [int(index) for index in similar_products_indices]

    # Get the 3 most similar products
    related_products = [all_products[index] for index in similar_products_indices]

    return render(request, 'product.html', {'product': chosen_product, 'relatedpr': related_products})

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
            if user.is_superuser:
                return redirect('/admin/')  # Redirect to the admin panel
            else:
                messages.success(request, "You have been logged in")
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
    products=Product.objects.filter(Q(name__icontains=query))
    return render(request,'searchproduct.html',{'products':products,'query':query})

def findgift(request):
    return render(request,'findgift.html',{})

def findcategory(request):
    try:
        query=request.GET.get('tusername')
        result=classifier(query)
        if result is None:
            return render(request,'gifts.html',{'categories':result})
        else:
            
            #list=[TECH, SPORTS , ARTS & CULTURE, WOMEN,BUSINESS,COMEDY,CRIME,EDUCATION,ENTERTAINMENT,ENVIRONMENT,MEDIA,POLITICS,RELIGION,SCIENCE]
            result1=[]
            for item in result:
                if item=="ARTS & CULTURE" or item=="ENTERTAINMENT"or item=="MEDIA":
                    result1.append("Music and Arts")
                elif item=="EDUCATION" or item=="ENVIRONMENT" or item=="POLITICS"or item=="RELIGION":
                    result1.append("Books")
                elif item=="WOMEN":
                    result1.append("Health and Beauty")
                    result1.append("Women's Fashion")
                elif item=="SPORTS":
                    result1.append("Sports and Outdoors")
                elif item=="TECH":
                    result1.append("Laptops and Gadgets")
                    result1.append("Home Appliances")
        
        categories_and_products = {}

        # Fetch products for each category
        for category_name in result1:
            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(category=category)[:2]  # Fetch the first two products for each category
            categories_and_products[category_name] = products

        return render(request, 'gifts.html', {'categories_and_products': categories_and_products,'tuser':query})
    except Exception as e:
        print(e)
        messages.success(request,("Tweets cant be extracted, Check the username and try again"))
        return redirect('findgift')

def myorders(request):
        # orders=Order.objects.get(name=request.User.username)
    
    orderss=Order.objects.filter(customer=request.user.username)
    print(orderss)
    return render(request,'myorders.html',{'orders':orderss})
      
    
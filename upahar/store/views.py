import os
from django.conf import settings
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
from .FinalTweetCategoryClassification import classifier,preprocess_tweet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .cossim import calc_cosine_similarity
from .tfidfvector import calculate_tf,calculate_tfidf,calculate_idf,tokenize
import numpy as np
import pandas as pd
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
    product_descriptions = [f"{chosen_product.name} - {chosen_product.description}"] + [f"{product.name} - {product.description}" for product in all_products]


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

    similar_scores = cosine_similarities[similar_products_indices]

    print(similar_scores)
    # Get the 3 most similar products
    related_products = [all_products[index] for index in similar_products_indices]

    product_with_score=zip(related_products,similar_scores)

    return render(request, 'product.html', {'product': chosen_product, 'relatedpr': product_with_score})

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
      
def findcategorynxt(request):
    #Tweet Classifier
    try:
        static_path = os.path.join(settings.STATICFILES_DIRS[0], 'usertweetswithhandle.csv')
        usertweets_df = pd.read_csv(static_path)
        query = request.GET.get('tusername')
        classification_report_str=classifier(query)
        X_tweets = usertweets_df.loc[usertweets_df['username'] == query, 'tweets']
        predicted_categories = usertweets_df.loc[usertweets_df['username'] == query, 'predicted_category']
        predicted_categories_str = predicted_categories.astype(str).tolist()
        print(predicted_categories_str)
        # Initialize an empty list to store the data for each tweet
        tweet_data = []

        # Assuming X_tweets contains the list of tweets
        for i,tweeto in enumerate(X_tweets):
            # Initialize an empty list to store related products for each tweet
            related_products_for_tweet = []
            print("-----------------------------")
            print(tweeto)
            print("-----------------------------")
            tweet=preprocess_tweet(tweeto)
            print("-----------------------------")
            # Extract product descriptions and combine with the tweet
            categor=predicted_categories_str[i]
            print(categor)
            category = Category.objects.get(name=categor)
            products = Product.objects.filter(category=category)
            product_descriptions = [tweet] + [f"{product.description}-{product.name}" for product in products]
            print("-----------------------------")
            print(product_descriptions)
            print("-----------------------------")
            # Calculate IDF
            idf = calculate_idf(product_descriptions)

            # Get sorted list of unique terms or vocabulary
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
            # Calculate cosine similarities with the tweet
            cosine_similarities = calc_cosine_similarity(tfidf_csr_matrix[-1], tfidf_csr_matrix[:-1])
            print("-----------------------------")
            print(cosine_similarities)
            # Get indices of the most similar products
            similar_products_indices = np.argsort(cosine_similarities)[::-1][:3]

            # Convert indices to integers
            similar_products_indices = [int(index) for index in similar_products_indices]

            similar_scores = cosine_similarities[similar_products_indices]
            print("-----------------------------")
            print(similar_products_indices)
            # Get the 3 most similar products
            related_products = [Product.objects.filter(category=category)[index] for index in similar_products_indices]

            # Append tweet data to the list
            tweet_data.append({
                'tweet': tweeto,
                'category':categor,
                'related_products': zip(related_products, similar_scores),
            })

        # Pass the tweet data to the template context
        context = {
            'tuser': query,
            'tweet_data': tweet_data,
            'classification_report': classification_report_str,
        }

        # Render the template with the context
        return render(request, 'giftsnxt.html', context)
    except Exception as e:
        print(e)
        messages.success(request,(e))
        return redirect('findgift')

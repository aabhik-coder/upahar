from audioop import reverse
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from .cart import Cart
from store.models import Product,Order
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CheckoutForm
import requests
import json
from django.conf import settings
from urllib.parse import urlencode

del_address=''
user_phone=''
# Create your views here.
def cart_summary(request):
    cart= Cart(request)
    cart_products=cart.get_prods
    quantity=cart.get_quants
    totals=cart.total()
    totalpaisa=totals*100
    return render(request,"cart.html",{'cart_products':cart_products,'quantities':quantity,'totals':totals,'totalpaisa':totalpaisa})

def cart_add(request):
    # get the cart
    cart=Cart(request)
    #test for post
    if request.POST.get('action')=='post':
        #get stuff
        product_id=int(request.POST.get('product_id'))
        product_quantity=int(request.POST.get('product_quantity'))
        #lookup for product
        product=get_object_or_404(Product,id=product_id)
        #save to a session
        cart.add(product=product,quantity=product_quantity)

        #return response
        response=JsonResponse({'Product Name':product.name})
        return response

def cart_delete(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        #get stuff
        product_id=int(request.POST.get('product_id'))
        #call delete function
        cart.delete(product=product_id)
        response=JsonResponse({'product':product_id})
        return response

def cart_update(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        #get stuff
        product_id=int(request.POST.get('product_id'))
        product_quantity=int(request.POST.get('product_quantity'))

        cart.update(product=product_id,quantity=product_quantity)

        response=JsonResponse({'qty':product_quantity})
        return response

def checkout_view(request):
    cart= Cart(request)
    cart_products=cart.get_prods()
    quantity=cart.get_quants()
    user_phone = request.session.get('user_phone', '')
    del_address = request.session.get('del_address', '')            
    print("from checkout")
    print(user_phone)
    print(del_address)
            # Create an order for each CartItem in the cart
    for cart_item in cart_products:
        # Retrieve quantity for the current cart item
        item_quantity = quantity.get(str(cart_item.id), 0)
        item_quantity = int(item_quantity)

        # Create an order
        order = Order.objects.create(
            product=cart_item,
            customer=request.user.username,  # Assuming Customer is a related model to User
            quantity=item_quantity,
            address=del_address,
            phone=user_phone,
            # Set other fields as needed
        )

        # Update product stock
        product = cart_item  # Assuming cart_item has a ForeignKey to Product
        product.stocks -= item_quantity
        product.save()

        # Remove the item from the cart
        cart.delete(cart_item.id)

    # Clear the cart after creating the orders

    return render(request, "orderconfirmation.html", {})   
             
def order_confirmation(request):
    return render(request,"orderconfirmation.html",{})

def init_khalti(request):
   try:
        if request.method == 'POST':
                form = CheckoutForm(request.POST)
                if form.is_valid():
                    url = "https://a.khalti.com/api/v2/epayment/initiate/"
                    return_url=request.POST.get('return_url')
                    purchase_order_id=request.POST.get('purchase_order_id')
                    amount=request.POST.get('amount')
                    
                    fname=request.POST.get('fname')
                    email=request.POST.get('email')
                    user_phone = form.cleaned_data['phone']
                    request.session['user_phone'] = user_phone
                    
                    del_address = form.cleaned_data['address']
                    request.session['del_address'] = del_address

                    payload = json.dumps({
                        "return_url": return_url,
                        "website_url": "http://127.0.0.1:8000/",
                        "amount": amount,
                        "purchase_order_id": purchase_order_id,
                        "purchase_order_name": "test",
                        "customer_info": {
                        "name": fname,
                        "email": email,
                        "phone":  user_phone
                        }
                    })
                    headers = {
                        'Authorization': "Key 6ed6f104da104798b1f05910966c9a84",
                        'Content-Type': 'application/json',
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)
                    #converting json into dictionary
                    new_res=json.loads(response.text)
                    print(new_res)
                    return redirect(new_res['payment_url'])
                else:
                    return render(request,'Formvalidationerror.html',{})
   except Exception as e:
        print(e)
        messages.success(request,("Enter a valid Phone number"))
        return redirect('cart_summary')

def verify_khalti(request):
    
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx=request.GET.get('pidx')
    headers = {
        'Authorization': "Key 6ed6f104da104798b1f05910966c9a84",
        'Content-Type': 'application/json',
    }

    payload = json.dumps({
        'pidx':pidx 
    })
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res=json.loads(response.text)
    print(new_res)
    
    return redirect('checkout_view')


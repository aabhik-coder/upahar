from django.shortcuts import redirect, render,get_object_or_404
from .cart import Cart
from store.models import Product,Order
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CheckoutForm


# Create your views here.
def cart_summary(request):
    cart= Cart(request)
    cart_products=cart.get_prods
    quantity=cart.get_quants
    totals=cart.total()
    return render(request,"cart.html",{'cart_products':cart_products,'quantities':quantity,'totals':totals})

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

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Get the logged-in user
            request.user

            # Create an order for each CartItem in the cart
            for cart_item in cart_products:
                # to retrieve quantity
                for key,value in quantity.items():
                    # convert key string into int
                    value=int(value)
                

               
                # Create an order
                order = Order.objects.create(
                    product=cart_item,
                    customer=request.user.username,  # Assuming Customer is a related model to User
                    quantity=value,
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                    # Set other fields as needed  # Adjust based on order processing logic
                )
                cart.delete(cart_item.id)
            # Clear the cart after creating the orders
            

            return redirect('order_confirmation')    
             
def order_confirmation(request):
    return render(request,"orderconfirmation.html",{})

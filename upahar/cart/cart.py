from store.models import Product

class Cart():
    def __init__(self,request):
        self.session=request.session
         
         # Get the current session key if it exists
        cart= self.session.get('session_key')

        #if the user is new , no session key
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        
        #making sure cart is available in all pages
        self.cart=cart

    def add(self,product):
        product_id=str(product.id)

        # logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]={'price':str(product.price)}

        self.session.modified=True

    def get_prods(self):
        #get ids from cart
        product_ids=self.cart.keys()
        #use ids to look up products
        products=Product.objects.filter(id__in=product_ids)
        #return products
        return products
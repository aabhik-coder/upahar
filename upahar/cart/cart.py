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

    def add(self,product,quantity):
        product_id=str(product.id)
        product_quantity=str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_quantity)

        self.session.modified=True

    def get_prods(self):
        #get ids from cart
        product_ids=self.cart.keys()
        #use ids to look up products
        products=Product.objects.filter(id__in=product_ids)
        #return products
        return products
    
    def get_quants(self):
        quantities=self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id= str(product)
        product_quantity=int(quantity)

        #get cart
        ourcart=self.cart
        #update dictionary/cart

        ourcart[product_id]=product_quantity
        self.session.modified=True
        
        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id=str(product)
        #delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified=True

    def total(self):
        #get product ids
        product_ids=self.cart.keys()
        #lookup keys in our  product database
        products=Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities=self.cart
        totl=0
        for key,value in quantities.items():
            # convert key string into int
            key=int(key)
            for product in products:
                if product.id==key:
                    totl = totl+(product.price)*value
        return totl

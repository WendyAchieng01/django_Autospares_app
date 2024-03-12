from auto.models import Product, Profile

class Cart(): 
    def __init__(self, request): 
        self.session = request.session


        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Cart works on all pages
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price: ': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in  user
        if self.request.user.is_authenticated:
            #Get the current User profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'",'\"')
            #Save carty to Profile Model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price: ': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in  user
        if self.request.user.is_authenticated:
            #Get the current User profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'",'\"')
            #Save carty to Profile Model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.offer:
                        total += int(product.sale_price * value)
                    else:
                        total += int(product.price * value)
        
        return total



    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()

        # Use ids tolook up poducts in DB
        products = Product.objects.filter(id__in=product_ids)

        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        self.cart[product_id] = quantity
        self.session.modified = True

        # Deal with logged in  user
        if self.request.user.is_authenticated:
            #Get the current User profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'",'\"')
            #Save carty to Profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        
        if product_id in  self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in  user
        if self.request.user.is_authenticated:
            #Get the current User profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'",'\"')
            #Save carty to Profile Model
            current_user.update(old_cart=str(carty))

    def render_checkout(self):
        checkout_data = {
            'cart_items': [],
            'total': 0
        }

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = {
                'id': product.id,
                'name': product.name,
                'quantity': self.cart[str(product.id)],
            }

            if product.offer:
                item['price'] = str(product.sale_price)
                item['total'] = str(product.sale_price * self.cart[str(product.id)])
                item['is_on_sale'] = True
            else:
                item['price'] = str(product.price)
                item['total'] = str(product.price * self.cart[str(product.id)])
                item['is_on_sale'] = False

            checkout_data['cart_items'].append(item)
            checkout_data['total'] += float(item['total'])

        return checkout_data
import json
from urllib.parse import urlencode
from django.shortcuts import redirect, render, get_object_or_404
from .cart import Cart
from auto.models import Product, Profile, ShippingAddress
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import ShippingForm, SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from orders.models import Order, OrderItem


# Create your views here. 
def cart_summary(request):

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()


    return render(request, "cart_summary.html", {'cart': cart, 'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

def cart_add(request): 
    # get cart 
    cart = Cart(request) 
    # test for POST 
    if request.method == 'POST' and request.POST.get('action') == 'post': 
        # get stuff 
        product_id = int(request.POST.get('product_id')) 
        product_qty = int(request.POST.get('product_qty')) 
        # look up product in DB 
        product = get_object_or_404(Product, id=product_id)

    # Save to session
    cart.add(product=product, quantity=product_qty)

    # Get Cart Quantity
    cart_quantity = len(cart)

    # Return response
    response = JsonResponse({'qty': cart_quantity})
    messages.success(request, ("Product Added To Cart..."))
    return response

def cart_delete(request): 
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response
    
def cart_update(request): 
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty', '')

        if product_qty:
            product_qty = int(product_qty)

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Your Cart HasBeen Updated..."))
        return response

@login_required
def checkout(request):
    cart = Cart(request)
    checkout_data = cart.render_checkout()

    submitted = False

    # Check if the user is logged in
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)

        # Populate initial data from user's profile
        initial_data = {
            'firstname': user_profile.user.first_name,
            'lastname': user_profile.user.last_name,
            'address': user_profile.address1,
            'city': '',
            'county': user_profile.county,
            'zipcode': user_profile.zipcode,
            'country': user_profile.country,
            'email': user_profile.user.email,
            'phonenumber': user_profile.phone,
            'note': '',
        }

        if request.method == "POST":
            form = ShippingForm(request.POST)
        else:
            form = ShippingForm(initial=initial_data)

        if form.is_valid():
            submitted = True
            user_profile.phone = form.cleaned_data['phonenumber']
            user_profile.save()

            # Create a new ShippingAddress instance and save it to the database
            shipping_address = ShippingAddress(
                user=request.user,
                firstname=form.cleaned_data['firstname'],
                lastname=form.cleaned_data['lastname'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                county=form.cleaned_data['county'],
                zipcode=form.cleaned_data['zipcode'],
                email=form.cleaned_data['email'],
                phonenumber=form.cleaned_data['phonenumber'],
                note=form.cleaned_data['note'],
            )
            shipping_address.save()

        # Create a new Order instance
            order = Order.objects.create(
                user=request.user,
                total_amount=float(checkout_data['total']),
                shipping_address=shipping_address,
            )

            # Create OrderItem instances for each item in the cart
            for item in checkout_data['cart_items']:
                product = Product.objects.get(id=item['id'])
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price'],
                )

            # Display a success message
            messages.success(request, 'Your order has been placed successfully.')    

            submitted_data = {
                'firstname': request.POST.get('firstname'),
                'lastname': request.POST.get('lastname'),
                'address': request.POST.get('address'),
                'city': request.POST.get('city'),
                'county': request.POST.get('county'),
                'zipcode': request.POST.get('zipcode'),
                'email': request.POST.get('email'),
                'phonenumber': request.POST.get('phonenumber'),
                'note': request.POST.get('note'),
            }

            
            # Store the submitted data in the session
            request.session['submitted_data'] = submitted_data

            # Redirect to the payment page
            return redirect('paymentdaraja:payment_page')

        else:
            initial_data = form.initial
    else:
        # If the user is not logged in, create an empty form
        form = ShippingForm()

    return render(request, "checkout1.html", {'checkout_data': checkout_data, 'form': form, 'cart': cart, 'submitted': submitted, 'phone_number': user_profile.phone if submitted else '','total': checkout_data['total'],})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from db
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert the dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop thru the cart and add the items from the db
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("You Have Been Logged In Successfully"))
            return redirect('index')
        else:
            messages.success(request, ("Username or Password Incorrect"))
            return redirect('cart:login')

    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been Logged out...Thanks for stopping by"))
    return redirect('index')

def register_user(request):
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please Fill Out Your User Info Below...")
            return redirect('cart:update_info')
    # If the form is not valid, render the registration page again with the errors
    return render(request, 'register.html', {'form': form})
       
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated")
            return redirect('index')
        return render(request, 'update_user.html', {'user_form':user_form})
    
    else: 
        messages.success(request, "You Must Be Logged In To Access Thid Paage!!")
        return redirect('index')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                #login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
        
    else: 
        messages.success(request, "You Must Be Logged In To View That Page!!!")
        return redirect('index')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Info Has Been Updated")
            return redirect('index')
        return render(request, 'update_info.html', {'form':form})
    
    else: 
        messages.success(request, "You Must Be Logged In To Access This Paage!!")
        return redirect('index')
    
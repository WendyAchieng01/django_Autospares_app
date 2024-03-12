# paymentdaraja/views.py

import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from urllib.parse import urlencode, parse_qs

from cart.cart import Cart
from paymentdaraja.models import Transaction

@login_required(login_url='cart:login')
def payment_index(request):
    # Get the cart instance
    cart = Cart(request)

    # Use the cart_total function to calculate the total amount
    amount = cart.cart_total()

    # Fetch the submitted data from the session
    submitted_data = request.session.get('submitted_data', {})

    # Use the phone number from the submitted data
    phone_number = submitted_data['phonenumber']

    # Rest of the parameters needed for the payment
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'

    # Create an instance of MpesaClient
    cl = MpesaClient()

    # Use the calculated amount and phone number in the stk_push function
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    
    if response is not None and response.response_code == '0':
        return JsonResponse({'success': True})
    else:
        error_message = response.response_description if response is not None else 'Unknown error'
        return JsonResponse({'success': False, 'error': error_message})

@login_required(login_url='cart:login')
def payment_stk_push_callback(request):
    data = json.loads(request.body)

    # Save the transaction details to the database
    transaction = Transaction(
        phone_number=data['phoneNumber'],
        amount=data['amount'],
        mpesa_receipt_number=data['mpesaReceiptNumber'],
        status=data['status']
    )
    transaction.save()

    return JsonResponse({"message": "STK Push in Django👋"})

@login_required(login_url='cart:login')
def payment_page(request):
    cart = Cart(request)
    checkout_data = cart.render_checkout()

    submitted_data = request.session.get('submitted_data', {})
    return render(request, "payment_page.html", {'checkout_data': checkout_data, 'submitted_data': submitted_data})

@login_required(login_url='cart:login')
def payment_success(request):
    return render(request, "payment_success.html")

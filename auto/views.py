from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from .models import *
from .models import Product
from django.db.models import Q
import decimal

# Create your views here.
def index(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    return render(request, 'index.html', {'categories': categories, 'brands': brands})

def contact(request):

    if request.method == 'POST':
        con_name = request.POST['con_name']
        con_email = request.POST['con_email']
        con_subject = request.POST['con_subject']
        con_message = request.POST['con_message']


    #send an email
        send_mail(
            con_subject,          # subject
            f"From: {con_name} <{con_email}>\n\n{con_message}",  # message
            con_email,            # from email
            ['rorenautomotors@gmail.com'],  # to email
        
            )
    

        return render(request, "contact.html", {'con_name': con_name})

    else:
        return render(request, "contact.html")
    

def about(request):

    return render(request, "about-us.html")

def shop(request):
    prods = Product.objects.all()
    categories = Category.objects.all()
    accessories = Accessories.objects.all()

    return render(request, 'shop.html', {'prods': prods, 'categories': categories, 'accessories': accessories})


def singleproduct(request, product_id):
    prod = Product.objects.get(pk=product_id)
    brands = Brand.objects.all()

    return render(request, 'single-product-variable.html', {'prod': prod, 'brands': brands})
    
def categorypage(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    prods_in_category = Product.objects.filter(category=category)
    accessories = Accessories.objects.all()

    return render(request, 'categorypage.html', {'category': category, 'prods': prods_in_category, 'accessories':accessories})

def brandpage(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    prods_in_brand = Product.objects.filter(brand=brand)
    accessories = Accessories.objects.all()

    return render(request, 'brandpage.html', {'brand': brand, 'prods': prods_in_brand, 'accessories':accessories})

def accessoriespage(request, accessories_id):
    accessories = get_object_or_404(Accessories, pk=accessories_id)
    prods_in_accessories = Product.objects.filter(accessories=accessories)
    all_accessories = Accessories.objects.all()

    return render(request, 'accessoriespage.html', {
        'accessories': accessories,
        'prods': prods_in_accessories,
        'accessories_list': all_accessories,
    })

def error_404(request, exception):

    return render(request, '404.html')


def faq(request):

    return render(request, 'faq.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def search_shop(request):
    accessories = Accessories.objects.all()

    if request.method == "POST":
        searched = request.POST['searched']
        prods = Product.objects.filter(Q(name__icontains=searched))


        return render(request, 'search_shop.html', {'searched': searched, 'prods': prods, 'accessories':accessories})
    else:
        return render(request, 'search_shop.html')
        
def specials(request):
    # Filter products with an offer
    prods = Product.objects.filter(offer=True)
    accessories = Accessories.objects.all()

    return render(request, 'specials.html', {'prods': prods, 'accessories': accessories})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def delivery(request):
    return render(request, 'delivery.html')

def terms_and_conditions(request):
    return render(request, 'tandc.html')

def returns(request):
    return render(request, 'returns.html')


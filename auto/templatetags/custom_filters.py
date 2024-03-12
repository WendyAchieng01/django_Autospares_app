from django import template
from auto.models import Product  

register = template.Library()

@register.filter(name='get_product')
def get_product(product_id):
    return Product.objects.get(pk=product_id)

# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_quantity')
def get_quantity(item):
    return item.get('quantity', '')

@register.filter(name='mult')
def mult(value, arg):
    return value * arg

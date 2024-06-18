# tienda/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def split_by_comma(value):
    if value:
        return value.split(',')
    return []



from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
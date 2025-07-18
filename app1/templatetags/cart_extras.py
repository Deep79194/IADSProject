from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return float(value) * float(arg) / 100

@register.filter
def add_tax(value, arg):
    return float(value) + (float(value) * float(arg)) / 100
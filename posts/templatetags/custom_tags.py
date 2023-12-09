from django import template
register = template.Library()

@register.filter
def concat(value, arg):
    return f'{value}{arg}'

@register.filter
def reverse(value):
    return reversed(value)

@register.filter
def reverse_and_slice(value, count):
    reversed_value = reversed(value)
    return list(reversed_value)[:count]
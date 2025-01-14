from django import template

register = template.Library()

# Custom filter to generate a range
@register.filter
def get_range(value):
    return range(1, value + 1)

# Custom filter to get an item from a dictionary using a tuple (row, col)
@register.filter
def get_item(value, args):
    return value.get(args, None)

from django import template
import math

register = template.Library()

@register.filter
def sub(val1, val2):
    return val1 - val2


@register.filter
def divCeil(val1, val2):
    return math.ceil(val1 / val2)
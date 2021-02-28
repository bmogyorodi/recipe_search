from django import template


register = template.Library()


@register.filter
def round_number(num):
    return round(num)

from django import template


register = template.Library()


@register.filter
def round_number(num):
    return round(num)


@register.filter
def is_within(ingredient, search_params):
    return any(x.lower() in ingredient for x in search_params["included_ingr"] + search_params["must_have"])


@register.simple_tag
def version():
    from django.conf import settings
    return settings.VERSION


@register.simple_tag
def commit_id():
    from django.conf import settings
    return settings.COMMIT_ID

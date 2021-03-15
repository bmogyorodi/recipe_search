from django import template


register = template.Library()


@register.filter
def round_number(num):
    return round(num)


@register.simple_tag
def version():
    from django.conf import settings
    return settings.VERSION


@register.simple_tag
def commit_id():
    from django.conf import settings
    return settings.COMMIT_ID

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def navactive(request, urls, arg=None):
    for url in urls.split():
        if arg is not None:
            rev = reverse(url, args=[arg])
        else:
            rev = reverse(url)
        try:
            if request.path == rev:
                return "active"
        except AttributeError:
            pass
    return ""


@register.filter
def mask_email(email):
    address, domain = email.split('@')
    return '@'.join([''.join(['*' for x in address]), domain])


@register.simple_tag
def divide(arg1, arg2):
    return int(arg1) / int(arg2)


@register.filter
def add_class(field, class_attr):
    if 'class' in field.field.widget.attrs:
        field.field.widget.attrs['class'] = '{} {}'.format(
            field.field.widget.attrs['class'],
            class_attr
        )
    else:
        field.field.widget.attrs['class'] = class_attr
    return field


@register.filter
def add_placeholder(field, placeholder):
    field.field.widget.attrs['placeholder'] = placeholder
    return field


@register.filter
def add_required(field):
    field.field.widget.attrs['required'] = 'required'
    return field

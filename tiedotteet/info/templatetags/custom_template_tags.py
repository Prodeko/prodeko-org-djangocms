# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from datetime import date

register = template.Library()


@register.filter(name='emailaddress', is_safe=True)
def emailaddress(value):
    return value.replace('@', '[at]')


@register.filter(name='is_past', is_safe=True)
def is_past(value):
    if date.today() > value:
        return True
    return False

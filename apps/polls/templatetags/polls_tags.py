import textwrap
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
@stringfilter
def charwrap(value, width):
    textwrapper = textwrap.TextWrapper(width=width,break_long_words=True,replace_whitespace=False)
    return textwrapper.fill(value)

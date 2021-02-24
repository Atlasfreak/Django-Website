import textwrap

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def index(indexable, i):
    """
    Return the value of a indexable at the specified index.
    """
    return indexable[i]


@register.filter
@stringfilter
def charwrap(value, width):
    textwrapper = textwrap.TextWrapper(
        width=width, break_long_words=True, replace_whitespace=False
    )
    return textwrapper.fill(value)


@register.filter
@stringfilter
def get_field_name(value: str):
    """
    Returns the name of the form field
    by splitting the value at every "-" character
    and returning the last part of that value.
    """
    splitted = value.split("-")
    return splitted[-1]

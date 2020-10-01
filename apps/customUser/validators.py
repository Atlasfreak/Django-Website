import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

class UnicodeFullNameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z\s][^\n\t\d]+\Z'
    message = _(
        'Please give your full name!'
    )
    flags = 0

class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
    )

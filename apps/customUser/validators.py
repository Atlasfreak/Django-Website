import re

from django.core import validators
from django.utils.translation import gettext_lazy as _

class UnicodeFullNameValidator(validators.RegexValidator):
    regex = r'^([ \u00c0-\u01ffa-z\'\-])+$'
    message = _(
        'Please give your full name!'
    )
    flags = re.IGNORECASE

class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
    )

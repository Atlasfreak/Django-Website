from importlib import import_module, resources

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ModuleValidator:
    valid_module_paths = []
    message = _("Please enter a valid Python module.")
    code = "invalid"

    def __init__(self, valid_module_paths=None, message=None, code=None):
        if valid_module_paths is not None:
            self.valid_module_paths = valid_module_paths
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """
        Validate that a given string is a valid python module path
        and that the given module exists.
        Check wether the given path is accepted.
        """
        try:
            module_path, class_name = value.rsplit(".", 1)
        except ValueError as err:
            raise ValidationError(
                _("%(value)s doesn't look like a valid module path."),
                self.code,
                params={"value": value},
            ) from err

        if (
            not (module_path in self.valid_module_paths)
            and self.valid_module_paths != []
        ):
            raise ValidationError(self.message, self.code)

        module = import_module(module_path)

        if not hasattr(module, class_name):
            raise ValidationError(self.message, self.code)

    def __eq__(self, other):
        return (
            isinstance(other, ModuleValidator)
            and self.valid_module_paths == other.module_str
            and self.message == other.message
            and self.code == other.code
        )


class FormWidgetValidator(ModuleValidator):
    valid_module_paths = ["django.forms.widgets", f"{__package__}.widgets"]
    message = _("Please enter a valid django form widget.")


class FormFieldValidator(ModuleValidator):
    valid_module_paths = [
        "django.forms.fields",
        f"{__package__}.fields",
        "django.forms.models",
    ]
    message = _("Please enter a valid django form field.")


class MaxNumberValidator(validators.MaxValueValidator):
    """Validates that no more than a given amount of options are selected."""

    message = _("Please do not select more than %(limit_value)s options.")
    code = "max_number"

    def clean(self, value: list):
        return len(value)


class MinNumberValidator(validators.MinValueValidator):
    """Validates that at least a given amount of options are selected."""

    message = _("Please select at least %(limit_value)s options.")
    code = "min_number"

    def clean(self, value: list):
        return len(value)

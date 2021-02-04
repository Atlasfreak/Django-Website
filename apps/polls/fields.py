from django.forms.models import ModelChoiceField, ModelMultipleChoiceField

from .validators import MaxNumberValidator, MinNumberValidator


class ModelListChoiceField(ModelChoiceField):
    def to_python(self, value):
        if not value:
            return list()
        return list(super().to_python(value))


class ModelLimitMultipleChoiceField(ModelMultipleChoiceField):
    """
    ModelMultipleChoiceField that can validate how boxes are check.
    """

    def __init__(self, queryset, max_number=None, min_number=None, **kwargs):
        super().__init__(queryset, **kwargs)
        self.max_number, self.min_number = max_number, min_number
        if max_number is not None:
            self.validators.append(MaxNumberValidator(max_number))
        if min_number is not None:
            self.validators.append(MinNumberValidator(min_number))

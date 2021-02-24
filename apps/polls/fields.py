from django.forms.models import ModelChoiceField, ModelForm, ModelMultipleChoiceField

from .validators import MaxNumberValidator, MinNumberValidator


class ModelListChoiceField(ModelChoiceField):
    def to_python(self, value):
        if not value:
            return list()
        return [
            super().to_python(value),
        ]


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


class CustomModelChoiceField(ModelChoiceField):
    """
    ModelChoiceField that converts strings via a dictionary to valid ids.
    Needed for a related question of :model:`polls.Choice`.

    Example:
        >>> from polls.models import Question
        >>> string_to_id = {"question-0": 1}
        >>> field = CustomModelChoiceField(Question.objects.get(id=1), string_to_id=string_to_id)
        >>> field.clean()
    """

    def __init__(self, queryset, *, string_to_id=None, **kwargs):
        if string_to_id is None:
            self.string_to_id = {}
        else:
            self.string_to_id = string_to_id
        super().__init__(queryset, **kwargs)

    def to_python(self, value):
        if self.string_to_id:
            value = self.string_to_id[value]
        return super().to_python(value)
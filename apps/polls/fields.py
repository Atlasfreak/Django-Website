from django.forms.models import ModelChoiceField


class ModelListChoiceField(ModelChoiceField):
    def to_python(self, value):
        return [super().to_python(value)]

from django import forms
from .fields import *
from .models import *


class ChoiceFormset(forms.BaseInlineFormSet):
    def __init__(self, *args, question_queryset, prefix_to_id=None, **kwargs):
        if prefix_to_id is None:
            self.prefix_to_id = {}
        else:
            self.prefix_to_id = prefix_to_id
        self.question_queryset = question_queryset

        super().__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["related_question"] = CustomModelChoiceField(
            self.question_queryset, string_to_id=self.prefix_to_id, required=False
        )


class AnswerModelFormset(forms.BaseModelFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        question = kwargs["questions"][index]
        kwargs.pop("questions")
        kwargs["question"] = question
        return kwargs

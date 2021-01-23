from django.forms.models import BaseModelFormSet


class AnswerModelFormset(BaseModelFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        question = kwargs["questions"][index]
        kwargs.pop("questions")
        kwargs["question"] = question
        return kwargs

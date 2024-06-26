import inspect

from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape, urlize
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from .models import (
    Answer,
    Choice,
    Poll,
    Question,
    QuestionType,
    QuestionTypeParam,
    Submission,
)


class PollCreationForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = (
            "title",
            "start_date",
            "end_date",
            "info_text",
            "multiple_votes",
            "is_public",
        )
        widgets = {"info_text": forms.Textarea()}


class QuestionTypeParamCreateForm(forms.ModelForm):
    class Meta:
        model = QuestionTypeParam
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        question_types = cleaned_data.get("question_type")
        attribute = cleaned_data.get("name")

        for type in question_types:
            field = type.get_field_class()
            params = inspect.getfullargspec(field).args
            param_count = len(params)
            if "self" in params:
                param_count -= 1

            if not hasattr(field(*[None] * param_count), attribute):
                raise ValidationError(
                    _("%(field)s does not have attribute: %(attribute)s."),
                    params={"field": type, "attribute": attribute},
                    code="invalid",
                )


def get_QuestionTypeParamForm(
    q_type_param: QuestionTypeParam,
    prefix: str = None,
    replace: str = None,
    *,
    data=None
):
    param_dict = q_type_param.get_param_dict()
    field_name = param_dict["name"]
    field: type[forms.Field] = param_dict["field"]

    Form: type[forms.Form] = type(
        "QuestionTypeParam_" + field_name + "_Form",
        (forms.Form,),
        {field_name: field(label=q_type_param.verbose_name, required=False)},
    )
    initial = {field_name: param_dict["default"]}
    if prefix is None:
        prefix = "__prefix__"
    if replace is not None:
        prefix = prefix.replace("__prefix__", replace)
    return Form(initial=initial, prefix=prefix, data=data)


def get_AnswerModelForm(self, question: Question, **kwargs):
    class AnswerForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            field_class = question.type.get_field_with_widget()

            params = {
                "label": urlize(escape(question.text), autoescape=True, nofollow=True),
                "required": question.required,
            }
            if question.extra_params:
                params.update(question.extra_params)
            if hasattr(field_class, "queryset"):
                params["queryset"] = question.choices.all()
            field = field_class(**params)

            if question.type.enable_choices:
                self.fields["choices"] = field
            else:
                self.fields["value"] = field
            self.instance.question = question

        class Meta:
            model = Answer
            if question.type.enable_choices:
                fields = ("choices",)
            else:
                fields = ("value",)

    return AnswerForm(**kwargs)


class AnswerFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.html5_required = True

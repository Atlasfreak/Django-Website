from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .forms import PollCreationForm
from .models import *

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    classes = ["collapse"]


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "title",
        "creation_date",
        "multiple_votes",
        "is_public",
    )
    list_filter = (
        "creator",
        "creation_date",
        "multiple_votes",
        "is_public",
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "creator",
                ],
            },
        ),
        (
            "Generelle Informationen:",
            {
                "fields": ["title", "info_text", "multiple_votes", "is_public"],
                "classes": ["collapse"],
            },
        ),
        ("Daten:", {"fields": ["start_date", "end_date"], "classes": ["collapse"]}),
    ]
    form = PollCreationForm
    inlines = [QuestionInline]
    search_fields = ["title"]


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "verbose_name",
        "form_field",
        "form_widget",
        "enable_choices",
    )
    list_filter = ("enable_choices",)


class QuestionTypeParamForm(forms.ModelForm):
    class Meta:
        model = QuestionTypeParam
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        question_types = cleaned_data.get("question_type")
        attribute = cleaned_data.get("name")

        for type in question_types:
            field = type.get_field_class()

            if not hasattr(field(), attribute):
                raise ValidationError(
                    _("%(field)s does not have attribute: %(attribute)s."),
                    params={"field": type, "attribute": attribute},
                    code="invalid",
                )


@admin.register(QuestionTypeParam)
class QuestionTypeParamAdmin(admin.ModelAdmin):
    list_display = ("name", "verbose_name", "default", "val_type")
    search_fields = ("name",)
    form = QuestionTypeParamForm


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "poll", "ip_adress", "submission_date")
    list_filter = ("user", "poll", "submission_date")

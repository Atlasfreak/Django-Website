from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import PollCreationForm, QuestionTypeParamCreateForm
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
        "results_public",
    )
    list_filter = (
        "creator",
        "creation_date",
        "multiple_votes",
        "is_public",
        "results_public",
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
                "fields": [
                    "title",
                    "info_text",
                    "multiple_votes",
                    "is_public",
                    "results_public",
                ],
            },
        ),
        ("Daten:", {"fields": ["start_date", "end_date"]}),
    ]
    form = PollCreationForm
    inlines = [QuestionInline]
    search_fields = ["title"]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question")
    list_filter = ("question",)


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "verbose_name",
        "form_field",
        "form_widget",
        "enable_choices",
    )
    list_filter = ("enable_choices",)


@admin.register(QuestionTypeParam)
class QuestionTypeParamAdmin(admin.ModelAdmin):
    list_display = ("name", "verbose_name", "default", "val_type")
    search_fields = ("name",)
    form = QuestionTypeParamCreateForm


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "poll", "ip_adress", "submission_date")
    list_filter = ("user", "poll", "submission_date")

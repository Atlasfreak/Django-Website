from django.contrib import admin

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
        "enable_choices",
        "form_widget",
        "form_field",
    )
    list_filter = ("enable_choices",)
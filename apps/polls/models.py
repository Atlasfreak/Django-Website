import secrets
from datetime import timedelta

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from .managers import PollManager, QuestionTypeManager
from .validators import FormFieldValidator, FormWidgetValidator

__all__ = [
    "Poll",
    "QuestionTypeParam",
    "QuestionType",
    "Question",
    "Choice",
    "Submission",
    "Answer",
]

USER_MODEL = settings.AUTH_USER_MODEL


def get_default_token():
    return secrets.token_urlsafe(7)


class Poll(models.Model):
    """
    Stores a poll that is related to a :model:`customUser.SiteUser`.
    For each poll there is an unique random base64 encoded 7 byte string token
    it is used to identify a poll from an URL.
    """

    creator = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="polls",
        verbose_name="Ersteller",
    )
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Erstellungsdatum"
    )
    start_date = models.DateTimeField(verbose_name="Startdatum")
    end_date = models.DateTimeField(
        verbose_name="Enddatum",
    )
    title = models.CharField(max_length=150, verbose_name="Titel")
    info_text = models.CharField(verbose_name="Beschreibung", max_length=2048)
    token = models.CharField(
        "Token für URL", max_length=32, unique=True, default=get_default_token
    )
    multiple_votes = models.BooleanField("Mehrmals Abstimmen")
    is_public = models.BooleanField("Öffentlich zugänglich")

    objects = PollManager()

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"

    def published_in_future(self):
        now = timezone.now()
        return now < self.start_date

    def ended(self):
        now = timezone.now()
        return now > self.end_date

    def is_published(self):
        return not (self.ended() or self.published_in_future())

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                {
                    "end_date": _("End date is before start date."),
                    "start_date": _("Start date is after end date."),
                },
                code="invalid",
            )

        if self.end_date - self.start_date < timedelta(days=1):
            raise ValidationError(
                {"end_date": _("End date is less than one day after start date.")},
                code="invalid",
            )

    def get_absolute_url(self):
        return reverse("polls:vote", kwargs={"token": self.token})

    def get_results_url(self):
        return reverse("polls:results", kwargs={"token": self.token})

    def __str__(self):
        return f"{self.title}"


class QuestionTypeParam(models.Model):
    """
    Connects a parameter of a form field to a :model:`polls.QuestionType` and
    adds the ability to change it for each question.
    Additionally it specifies how to convert the input into python types and
    which field should be displayed for that type.

    Vars:
        -   "TYPE_CHOICES" are the choices for the val_type
        -   "STRING_TO_FUNCTION" maps the different string representations of types
            to their respective python types and form fields
        -   "name" is the exact name of the parameter for the form field of the
            :model:`polls.QuestionType`
        -   "verbose_name" is a human readable name that is displayed when creating a poll
        -   "question_type" is the connected :model:`polls.QuestionType`
        -   "default" is the default value that should be used for that parameter
        -   "val_type" specifies how to convert the input to a python type
    """

    TYPE_STRING = "str"
    TYPE_INT = "int"
    TYPE_FLOAT = "float"
    TYPE_BOOL = "bool"

    CONVERTER_KEY = "converter"
    FIELD_KEY = "field"

    TYPE_CHOICES = [
        (TYPE_INT, "Integer"),
        (TYPE_STRING, "String"),
        (TYPE_BOOL, "Boolean"),
        (TYPE_FLOAT, "Decimal"),
    ]

    STRING_TO_FUNCTION = {
        TYPE_STRING: {CONVERTER_KEY: str, FIELD_KEY: forms.CharField},
        TYPE_INT: {CONVERTER_KEY: int, FIELD_KEY: forms.IntegerField},
        TYPE_BOOL: {CONVERTER_KEY: bool, FIELD_KEY: forms.BooleanField},
        TYPE_FLOAT: {CONVERTER_KEY: float, FIELD_KEY: forms.DecimalField},
    }

    name = models.CharField(_("Parameter Name"), max_length=128)
    verbose_name = models.CharField(
        _("Lesbarer Name, wird dem Nutzer angezeigt"), max_length=50
    )
    question_type = models.ManyToManyField(
        "QuestionType",
        verbose_name=_("Zugehöriger Frage Typ"),
        related_name="params",
    )
    default = models.CharField(_("Standardwert"), max_length=128, blank=True, null=True)

    val_type = models.CharField(
        _("Typ der Eingabewerte"),
        max_length=128,
        choices=TYPE_CHOICES,
    )

    class Meta:
        verbose_name = _("QuestionTypeParam")
        verbose_name_plural = _("QuestionTypeParams")

    def get_converter(self):
        converter = self.STRING_TO_FUNCTION[self.val_type][self.CONVERTER_KEY]
        return converter

    def get_field(self):
        field: type[forms.Field] = self.STRING_TO_FUNCTION[self.val_type][self.FIELD_KEY]
        return field

    def get_param_dict(self):  # deprecated
        """Returns all necessary variables for a form. Should be deleted..."""
        param_dict = {}
        converter = self.get_converter()
        param_dict["converter"] = converter
        param_dict["field"] = self.get_field()
        param_dict["default"] = converter(self.default) if self.default else None
        param_dict["name"] = self.name
        return param_dict

    def __str__(self):
        return self.verbose_name


class QuestionType(models.Model):
    """
    Describes the different types of :model:`polls.Question` and declares their representation in forms when a poll is answered.

    Vars:

        -   "verbose_name" is a human_readable name that is displayed when creating a new poll.

        -   "enable_choices" specifies whether there should be choices available to this type,
            for example when the user should be able to select from a range of choices.
            If choices are enabled at least one choice needs to be given to a question.

        -   "form_widget" is the Django form widget to use, if blank it is the default for the field.

        -   "form_field" is the Django form field to use.
    """

    form_widget_validator = FormWidgetValidator()
    form_field_validator = FormFieldValidator()

    verbose_name = models.CharField("Lesbarer Name", max_length=50)
    enable_choices = models.BooleanField("Optionen verfügbar", default=True)
    form_widget = models.CharField(
        "Django Form Widget Klassen Pfad",
        max_length=255,
        help_text='Vollständiger Pfad zu einem Widget z.B. "django.forms.widgets.TextInput".',
        validators=[form_widget_validator],
        blank=True,
    )
    form_field = models.CharField(
        "Django Form Field Klassen Pfad",
        max_length=255,
        help_text='Vollständiger Pfad zu einem Field z.B. "django.forms.fields.CharField".',
        validators=[form_field_validator],
        default="django.forms.fields.CharField",
    )

    objects = QuestionTypeManager()

    class Meta:
        verbose_name = "QuestionType"
        verbose_name_plural = "QuestionTypes"

    def get_widget_class(self):
        widget_path = self.form_widget
        widget: type[forms.Widget] = import_string(widget_path)
        return widget

    def get_field_class(self):
        field_path = self.form_field
        field: type[forms.Field] = import_string(field_path)
        return field

    def get_field_with_widget(self, **params):
        base_field = self.get_field_class()
        # Create a new field class so I do not override the widget for all fields of that type
        field: type[forms.Field] = type("Poll" + base_field.__name__, (base_field,), {**params})
        field.widget = self.get_widget_class() if self.form_widget else field.widget
        return field

    def get_id_to_param(self):
        """Returns a dict which maps the question type id to the names of its parameters."""
        id = self.pk
        params = list(self.params.values_list("name", flat=True))
        if not params:
            return {}
        return {id: params}

    def __str__(self):
        return f"{self.verbose_name}"


class Question(models.Model):
    """
    Stores a question that is related to a :model:`polls.Poll` and
    a :model:`polls.QuestionType`.
    """

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="zugehörige Umfrage",
    )
    text = models.CharField(max_length=128, verbose_name="Frage")
    required = models.BooleanField(verbose_name="erforderlich", default=False)
    type = models.ForeignKey(
        QuestionType, verbose_name="Fragetyp", on_delete=models.CASCADE
    )
    results_public = models.BooleanField(
        "Ergebnisse öffentlich zugänglich", default=False
    )
    extra_params = models.JSONField("Extra Parameter für Frage", blank=True, null=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.text}"


class Choice(models.Model):
    """
    Stores a choice related to :model:`polls.Question`
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="zugehörige Frage",
    )
    text = models.CharField(max_length=128, verbose_name="Option")

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return f"{self.text}"


class Submission(models.Model):
    """
    Stores a submission for a :model:`polls.Poll` from a :model:`customUser.SiteUser`.
    Ip adresses should only be stored if a poll does not allow multiple votes.
    """

    user = models.ForeignKey(
        USER_MODEL,
        verbose_name="Nutzer",
        on_delete=models.CASCADE,
        related_name="submissions",
        blank=True,
        null=True,
    )
    poll = models.ForeignKey(
        Poll,
        verbose_name="Umfrage",
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    ip_adress = models.GenericIPAddressField(
        "IP-Adresse der Einreichung",
        protocol="both",
        unpack_ipv4=False,
        blank=True,
        null=True,
    )
    submission_date = models.DateTimeField(
        "Einsendedatum", auto_now=True, auto_now_add=False
    )

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self):
        return f"{self.user}-{self.poll}"


class Answer(models.Model):
    """
    Stores a answer to a :model:`polls.Question` that belongs to
    a :model:`polls.Submission`.
    There is a m2m relationship to :model:`polls.Choice` as there
    can be multiple choice questions and this simplifies the database.
    Choices are optional.
    """

    submission = models.ForeignKey(
        Submission,
        verbose_name="Einsendung",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question, verbose_name="Frage", on_delete=models.CASCADE, related_name="answers"
    )
    choices = models.ManyToManyField(
        Choice,
        verbose_name="Antwortkey",
        related_name="answers",
    )
    value = models.CharField("Antwortwert", max_length=2048, blank=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f"{self.value}"

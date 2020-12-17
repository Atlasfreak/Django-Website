import secrets
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.module_loading import import_string
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from apps.customUser.models import SiteUser

from .validators import FormWidgetValidator

# Create your models here.

def get_default_token():
    return secrets.token_urlsafe(7)

def get_past_date():
    return timezone.now() - timedelta(minutes=30.0)

class Poll (models.Model):
    general_date_validator = MinValueValidator((get_past_date), message=_('The date lies in the past.'))

    creator = models.ForeignKey(SiteUser, on_delete = models.CASCADE, related_name = 'polls', verbose_name = 'Ersteller')
    creation_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Erstellungsdatum')
    start_date = models.DateTimeField(verbose_name = 'Startdatum')
    end_date = models.DateTimeField(verbose_name = 'Enddatum', validators=[general_date_validator])
    title = models.CharField(max_length = 150, verbose_name = 'Titel')
    info_text = models.CharField(verbose_name = 'Beschreibung', max_length=2048)
    token = models.CharField('Token für url', max_length = 32, unique=True, default=get_default_token)
    multiple_votes = models.BooleanField('Mehrmals Abstimmen')

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError({
                            'end_date': _('End date is before start date.'),
                            'start_date': _('Start date is after end date.'),
            }, code = 'invalid')
        
        if self.end_date - self.start_date < timedelta(days=1):
            raise ValidationError({'end_date':_('End date is less than one day after start date.')}, code = 'invalid')

    def get_absolute_url(self):
        return reverse('polls:vote', kwargs={'token': self.token})

    def __str__(self):
        return f'{self.title}'


class QuestionType(models.Model):
    form_widget_validator = FormWidgetValidator()

    html_input_type = models.CharField('HTML Input Typ', max_length=10)
    verbose_name = models.CharField('Lesbarer Name', max_length=50)
    enable_choices = models.BooleanField('Optionen verfügbar', default=True)
    form_widget = models.CharField(
        'Django Form Widget Klassen Pfad',
        max_length=255,
        help_text='Vollständiger Pfad zu einem Widget z.B. "django.forms.widgets.TextInput".',
        validators=[form_widget_validator],
        )

    class Meta:
        verbose_name = 'QuestionType'
        verbose_name_plural = 'QuestionTypes'

    def get_widget_class(self):
        widget_path = self.form_widget
        widget = import_string(widget_path)
        return widget

    def __str__(self):
        return f'{self.verbose_name}'


class Question (models.Model):
    poll = models.ForeignKey(Poll, on_delete = models.CASCADE, related_name = 'question', verbose_name = 'zugehörige Umfrage')
    text = models.CharField(max_length = 128, verbose_name = 'Frage')
    required = models.BooleanField(verbose_name = 'erforderlich', default = False)

    type = models.ForeignKey(QuestionType, verbose_name='Fragetyp', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'{self.text}'


class Choice (models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'choices', verbose_name = 'zugehörige Frage')
    text = models.CharField(max_length = 128, verbose_name = 'Option')

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    def __str__(self):
        return f'{self.text}'


class Submission(models.Model):
    user = models.ForeignKey(SiteUser, verbose_name='Nutzer', on_delete=models.CASCADE, related_name = 'submission')
    poll = models.ForeignKey(Poll, verbose_name='Umfrage', on_delete=models.CASCADE, related_name = 'submission')
    ip_adress = models.GenericIPAddressField('IP-Adresse der Einreichung', protocol='both', unpack_ipv4=False)
    submission_date = models.DateTimeField('Einsendedatum', auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'

    def __str__(self):
        return f'{self.user}-{self.poll}'


class Answer (models.Model):
    submission = models.ForeignKey(SiteUser, verbose_name='Einsendung', on_delete=models.CASCADE, related_name = 'answer')
    question = models.ForeignKey(Question, verbose_name='Frage', on_delete=models.CASCADE, related_name = 'answer')
    choice = models.ForeignKey(Choice, verbose_name='Antwortkey', on_delete=models.CASCADE, related_name = 'answer')
    value = models.CharField('Antwortwert', max_length=2048)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f'{self.value}'

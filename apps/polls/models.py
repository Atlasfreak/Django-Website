from apps.customUser.validators import UnicodeFullNameValidator
from django.db import models

from apps.customUser.models import SiteUser

# Create your models here.

class Polls (models.Model):
    creator = models.ForeignKey(SiteUser, on_delete = models.CASCADE, related_name = 'polls', verbose_name = 'Ersteller')
    creation_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Erstellungsdatum')
    start_date = models.DateTimeField(verbose_name = 'Startdatum')
    end_date = models.DateTimeField(verbose_name = 'Enddatum')
    title = models.CharField(max_length = 150, verbose_name = 'Titel')
    token = models.CharField('token für url', max_length = 32)

class Question (models.Model):
    poll = models.ForeignKey(Polls, on_delete = models.CASCADE, related_name = 'question', verbose_name = 'zugehörige Umfrage')
    text = models.CharField(max_length = 128, verbose_name = 'Fragetext')
    required = models.BooleanField(verbose_name = 'benötigt', default = False)

    TEXTFIELD = 'TF'
    DATEFIELD = 'DF'
    CHECKBOX = 'CB'
    RADIO = 'RD'

    TYPE_CHOICES = [
        (TEXTFIELD, 'textarea'),
        (DATEFIELD, 'date'),
        (CHECKBOX, 'checkbox'),
        (RADIO, 'radio')
    ]

    type = models.CharField('Fragetyp', max_length = 150, choices = TYPE_CHOICES)

class Choices (models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'choices', verbose_name = 'zugehörige Frage')
    text = models.CharField(max_length = 256, verbose_name = 'Auswahltext')
    help_text = models.CharField(verbose_name = 'Eingabe Hilfe Text', max_length= 128)

class Answers (models.Model):
    question = models.ForeignKey(Question, verbose_name='Frage', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, verbose_name='Antwortkey', on_delete=models.CASCADE, related_name = 'answers')
    value = models.TextField('Antwortwert')
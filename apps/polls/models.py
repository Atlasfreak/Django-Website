from django.db.models.fields import CharField
from apps.customUser.validators import UnicodeFullNameValidator
from django.db import models

from apps.customUser.models import SiteUser

# Create your models here.

class Poll (models.Model):
    creator = models.ForeignKey(SiteUser, on_delete = models.CASCADE, related_name = 'polls', verbose_name = 'Ersteller')
    creation_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Erstellungsdatum')
    start_date = models.DateTimeField(verbose_name = 'Startdatum')
    end_date = models.DateTimeField(verbose_name = 'Enddatum')
    title = models.CharField(max_length = 150, verbose_name = 'Titel')
    token = models.CharField('token für url', max_length = 32)
    multiple_votes = models.BooleanField('Mehrmals Abstimmen')

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"

    def __str__(self):
        return f'{self.title}'


class Question (models.Model):
    poll = models.ForeignKey(Poll, on_delete = models.CASCADE, related_name = 'question', verbose_name = 'zugehörige Umfrage')
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

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f'{self.text}'


class Choice (models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'choices', verbose_name = 'zugehörige Frage')
    text = models.CharField(max_length = 256, verbose_name = 'Auswahltext')
    help_text = models.CharField(verbose_name = 'Eingabe Hilfe Text', max_length= 128)

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return f'{self.text}'


class Submission(models.Model):
    user = models.ForeignKey(SiteUser, verbose_name='Nutzer', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, verbose_name='Umfrage', on_delete=models.CASCADE)
    ip_adress = models.GenericIPAddressField('IP-Adresse der Einreichung', protocol="both", unpack_ipv4=False)
    submission_date = models.DateTimeField('Einsendedatum', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self):
        return f'{self.user}'


class Answer (models.Model):
    submission = models.ForeignKey(SiteUser, verbose_name='', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Frage', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, verbose_name='Antwortkey', on_delete=models.CASCADE, related_name = 'answers')
    value = models.CharField('Antwortwert', max_length=2048)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f'{self.value}'

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
    info_text = models.CharField(verbose_name = 'Beschreibung', max_length=2048)
    token = models.CharField('Token für url', max_length = 32)
    multiple_votes = models.BooleanField('Mehrmals Abstimmen')

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return f'{self.title}'


class QuestionType(models.Model):

    html_input_type = models.CharField('HTML Input Typ', max_length=10)
    verbose_name = models.CharField('Lesbarer Name', max_length=50)

    class Meta:
        verbose_name = 'QuestionType'
        verbose_name_plural = 'QuestionTypes'

    def __str__(self):
        return f'{self.verbose_name}'


class Question (models.Model):
    poll = models.ForeignKey(Poll, on_delete = models.CASCADE, related_name = 'question', verbose_name = 'zugehörige Umfrage')
    text = models.CharField(max_length = 128, verbose_name = 'Frage')
    required = models.BooleanField(verbose_name = 'erforderlich', default = False)

    # LITTLETEXT = 'text'
    # TEXT = 'textarea'
    # DATEFIELD = 'date'
    # CHECKBOX = 'checkbox'
    # RADIO = 'radio'
    # SELECT = 'select'

    # TYPE_CHOICES = [
    #     (TEXT, 'Langer Text'),
    #     (LITTLETEXT, 'Kurzer Text'),
    #     (DATEFIELD, 'Datum'),
    #     (CHECKBOX, 'Mehrfachauswahl'),
    #     (RADIO, 'Einzelauswahl'),
    #     (SELECT, 'Dropdown'),
    # ]

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
        return f'{self.user}'


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


from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Choice

@receiver(pre_delete, sender=Choice)
def pre_delete_choice(sender, instance, **kwargs):
    '''
    Delete Answer if the last corresponding choice gets deleted.
    '''
    for answer in instance.answers.all():
        if answer.choices.count() == 1:
            answer.delete()
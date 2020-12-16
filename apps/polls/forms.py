from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Poll, Question, Choice, Answer, Submission

class PollCreationForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'start_date', 'end_date', 'info_text', 'multiple_votes')
        widgets = {'info_text': forms.Textarea()}
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from .models import Poll, Question, Choice, Answer, Submission

class PollCreationForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'start_date', 'end_date', 'info_text', 'multiple_votes')
        widgets = {'info_text': forms.Textarea()}


def get_AnswerModelForm(self, question, **kwargs):
    class AnswerForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            field_class = question.type.get_field_with_widget()

            params = {'label': question.text, 'required': question.required}
            if hasattr(field_class, 'queryset'):
                params['queryset'] = question.choices.all()
            field = field_class(**params)
            if question.type.enable_choices:
                self.fields['choices'] = field
            else:
                self.fields['value'] = field
            self.instance.question = question

        class Meta:
            model = Answer
            if question.type.enable_choices:
                fields = ('choices',)
                
            else:
                fields = ('value',)

    return AnswerForm(**kwargs)
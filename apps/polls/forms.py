from django import forms

from .models import Poll, Question, Choice, Answer, Submission

class PollCreationForm(forms.ModelForm):
    
    inf_text = forms.CharField(max_length=2048, required=True, widget=forms.Textarea)

    class Meta:
        model = Poll
        fields = ('title', 'start_date', 'end_date', 'info_text', 'multiple_votes')
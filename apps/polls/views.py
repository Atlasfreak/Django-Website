from django.contrib import messages
from django.http import request
from django.shortcuts import render
from django.forms import inlineformset_factory

from .forms import *
from .models import *

# Create your views here.

def index(request):
    pass

def create(request):
    QuestionInlineFormset = inlineformset_factory(Poll, Question, fields = ('text', 'type', 'required',), max_num = 100, can_delete = False, extra = 1,)
    question_formset = QuestionInlineFormset(prefix='question')
    choice_formset_list = []
    ChoiceInlineFormset = inlineformset_factory(Question, Choice, fields = ('text',), max_num = 100, extra = 1, can_delete = False,)

    empty_choice_formset = ChoiceInlineFormset(prefix=f'{question_formset.empty_form.prefix}-choice')
    
    if request.method == 'POST':
        poll_form = PollCreationForm(request.POST, prefix='poll')
        print(request.POST)
        if poll_form.is_valid():
            # poll_form.save()
            question_formset = QuestionInlineFormset(request.POST, prefix='question')
            if question_formset.is_valid():
                for form in question_formset:
                    prefix = f'{form.prefix}-choice'
                    data_choice_formset = ChoiceInlineFormset(request.POST, prefix=prefix)
                    if data_choice_formset.is_valid():
                        pass
                    choice_formset_list.append(data_choice_formset)

                messages.success(request, 'Umfrage erfolgreich erstellt.')
    else:
        poll_form = PollCreationForm(prefix='poll')
    
        for form in question_formset:
            prefix = f'{form.prefix}-choice'
            choice_formset_list.append(ChoiceInlineFormset(prefix=prefix))
    

    options_deactivated = list(QuestionType.objects.filter(enable_choices = False).values_list('id', flat=True))

    context = {
        'poll_form' : poll_form,
        'question_formset': question_formset,
        'choice_formset_list': choice_formset_list,
        'empty_choice_formset': empty_choice_formset,
        'options_deactivated': options_deactivated,
    }
    return render(request, 'polls/polls_create.html', context)

def vote(request, token):
    pass

def results(request, token):
    pass

def edit(request, token):
    pass
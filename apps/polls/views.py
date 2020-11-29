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
    QuestionInlineFormset = inlineformset_factory(Poll, Question, fields = ('text', 'type', 'required',), max_num = 100, can_delete = False,)
    question_formset = QuestionInlineFormset(prefix='question')
    choice_formset_list = []
    ChoiceInlineFormset = inlineformset_factory(Question, Choice, fields = ('text',), max_num = 100, extra = 1, can_delete = False,)

    for form in question_formset:
        prefix = f'{form.prefix}-choice'
        choice_formset_list.append(ChoiceInlineFormset(prefix=prefix))
    
    empty_choice_formset = ChoiceInlineFormset(prefix=f'{question_formset.empty_form.prefix}-choice')
    
    if request.method == 'POST':
        poll_form = PollCreationForm(request.POST)
        print(request.POST)
        if poll_form.is_valid():
            # poll_form.save()
            messages.success(request, 'Umfrage erfolgreich erstellt.')
    else:
        poll_form = PollCreationForm()

    context = {
        'poll_form' : poll_form,
        'question_formset': question_formset,
        'choice_formset_list': choice_formset_list,
        'empty_choice_formset': empty_choice_formset,
    }
    return render(request, 'polls/polls_create.html', context)

def vote(request, token):
    pass

def results(request, token):
    pass

def edit(request, token):
    pass
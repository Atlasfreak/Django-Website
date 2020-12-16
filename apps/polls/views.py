import secrets

from django.contrib import messages
from django.http import request
from django.shortcuts import render
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .forms import *
from .models import *
# Create your views here.

def index(request):
    pass

@login_required
def create(request):
    QuestionInlineFormset = inlineformset_factory(Poll, Question, fields = ('text', 'type', 'required',), max_num = 100, can_delete = False, extra = 1,)
    
    choice_formset_list = []
    ChoiceInlineFormset = inlineformset_factory(Question, Choice, fields = ('text',), max_num = 100, min_num=1, extra = 0, can_delete = False,)

    poll_form = PollCreationForm(prefix='poll')
    
    question_formset = QuestionInlineFormset(prefix='question')

    options_deactivated = list(QuestionType.objects.filter(enable_choices = False).values_list('id', flat=True))

    if request.method == 'POST':
        
        poll_form = PollCreationForm(request.POST, prefix='poll')
            question_formset = QuestionInlineFormset(request.POST, prefix='question')

        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.token = secrets.token_urlsafe(7)
            poll.creator = request.user
            question_formset.instance = poll
            
            if question_formset.is_valid():
                choices_valid = True
                for form in question_formset:
                    prefix = f'{form.prefix}-choice'
                    if form.cleaned_data:
                        if form.cleaned_data['type'].enable_choices:
                            form_saved = form.save(commit=False)
                            data_choice_formset = ChoiceInlineFormset(request.POST, prefix=prefix, instance=form_saved)
                            
                            choices_valid &= data_choice_formset.is_valid()
                    choice_formset_list.append(data_choice_formset)
                        else:
                            choice_formset_list.append(ChoiceInlineFormset(prefix=prefix))
                    else:
                        choice_formset_list.append(ChoiceInlineFormset(prefix=prefix))

                if choices_valid:
                    poll.save()
                    question_formset.save()
                    for formset in choice_formset_list:
                        formset.save()
                    context = {
                                'poll': poll,
                            }
                    return render(request, 'polls/polls_create_complete.html', context)
    else:
                for form in question_formset:
                    prefix = f'{form.prefix}-choice'
                    data_choice_formset = ChoiceInlineFormset(request.POST, prefix=prefix)
                    choice_formset_list.append(data_choice_formset)
    
    if choice_formset_list == []:
        for form in question_formset:
            prefix = f'{form.prefix}-choice'
            choice_formset_list.append(ChoiceInlineFormset(prefix=prefix))
    
    empty_choice_formset = ChoiceInlineFormset(prefix=f'{question_formset.empty_form.prefix}-choice')

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
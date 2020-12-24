import secrets

from django.contrib import messages
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .forms import *
from .models import *
# Create your views here.

def index_view(request):
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
            poll.creator = request.user
            question_formset.instance = poll
            
            if question_formset.is_valid():
                choices_valid = True
                for form in question_formset:
                    prefix = f'{form.prefix}-choice'
                    choice_formset=ChoiceInlineFormset(prefix=prefix)
                    if form.cleaned_data:
                        if form.cleaned_data['type'].enable_choices:
                            form_saved = form.save(commit=False)
                            data_choice_formset = ChoiceInlineFormset(request.POST, prefix=prefix, instance=form_saved)
                            
                            choices_valid &= data_choice_formset.is_valid()
                            choice_formset=data_choice_formset

                    choice_formset_list.append(choice_formset)
                
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
    poll = Poll.objects.get(token=token)
    
    if not poll.is_published():
        message = 'Diese Umfrage ist nicht öffentlich.'
        if poll.ended():
            message = 'Diese Umfrage ist beendet.'
        elif poll.published_in_future():
            message = 'Diese Umfrage hat noch nicht gestartet.'
        return render(request, 'polls/poll_error.html', context={'message': message})
    
    questions = poll.questions.all()

    question_list = list(questions)

    Formset = modelformset_factory(Answer, fields=('value',), extra=len(question_list))
    real_formset = Formset(queryset=Answer.objects.none())
    
    for i in range(len(real_formset)):
        init_form = real_formset.forms[i]
        replace_form = get_AnswerModelForm(question_list[i])(prefix=init_form.prefix)
        real_formset.forms[i] = replace_form

    if request.method == 'POST':
        real_formset = Formset(request.POST)
        
        for i in range(len(real_formset)):
            init_form = real_formset.forms[i]
            replace_form = get_AnswerModelForm(question_list[i])(prefix=init_form.prefix, data=init_form.data)
            real_formset.forms[i] = replace_form
        
        if real_formset.is_valid():
            instances = real_formset.save(commit=False)
            submission, created = Submission.objects.get_or_create(user=request.user, poll=poll)
            for form in real_formset.forms:
                print(form.prefix, form.cleaned_data)
            if not poll.multiple_votes:
                submission.ip_adress = request.META.get('REMOTE_ADDR')
                request.session['has_voted'] = True
            for instance in instances:
                instance.submission = submission
                instance.question = question_list[instances.index(instance)]
                instance.save()
            real_formset.save_m2m()
        else:
            print(real_formset.non_form_errors)
            print(real_formset.errors)

    context = {
        'poll': poll,
        'formset': real_formset,
    }
    return render(request, 'polls/polls_vote.html', context)

def results(request, token):
    pass

def edit(request, token):
    pass
import csv
import textwrap

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory, formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .decorators import is_creator
from .forms import *
from .formset import AnswerModelFormset
from .models import *
# Create your views here.

def index_view(request):
    user = request.user
    user_polls = []
    if user.is_authenticated:
        user_polls = Poll.objects.filter(creator=user).order_by('-start_date')
    all_polls = Poll.objects.are_published().filter(is_public=True).order_by('-start_date')
    
    context = {
        'user_polls': user_polls,
        'all_polls': all_polls,
    }
    return render(request, 'polls/polls_index.html', context)

@login_required
def create(request):
    QuestionInlineFormset = inlineformset_factory(Poll, Question, fields = ('text', 'type', 'required',), max_num = 100, min_num=1, can_delete = False, extra = 0,)
    
    ChoiceInlineFormset = inlineformset_factory(Question, Choice, fields = ('text',), max_num = 100, min_num=1, extra = 0, can_delete = False,)

    options_deactivated = list(QuestionType.objects.filter(enable_choices = False).values_list('id', flat=True))

    choice_formset_list = []

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
    else:
        poll_form = PollCreationForm(prefix='poll')

        question_formset = QuestionInlineFormset(prefix='question')

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
    ip_adress = request.META.get('REMOTE_ADDR')

    if not poll.is_published():
        message = 'Diese Umfrage ist nicht öffentlich.'
        if poll.ended():
            message = 'Diese Umfrage ist beendet.'
        elif poll.published_in_future():
            message = 'Diese Umfrage hat noch nicht gestartet.'
        messages.error(request, message)
        return redirect('polls:index')
    
    has_voted = False
    if (cookie := request.session.get('has_voted', False)):
        if cookie.get(poll.id, False):
            has_voted = True

    if not poll.multiple_votes and (has_voted or Submission.objects.filter(ip_adress=ip_adress, poll=poll).exists()):
        message = 'Du hast für diese Umfrage bereits abgestimmt!'
        messages.error(request, message)
        return redirect('polls:index')

    questions = poll.questions.all()

    question_list = list(questions)

    Formset = formset_factory(get_AnswerModelForm, formset=AnswerModelFormset,extra=0, min_num=questions.count())
    Formset.model = Answer
    formset_params = {'form_kwargs': {'questions': question_list}}

    if request.method == 'POST':
        real_formset = Formset(request.POST, **formset_params)

        if real_formset.is_valid():
            instances = real_formset.save(commit=False)
            user = request.user

            submission_params = {}
            if not poll.multiple_votes:
                submission_params['ip_adress'] = ip_adress
                
                cookie = request.session.get('has_voted', False)
                if not cookie:
                    request.session['has_voted'] = {}
                    cookie = request.session['has_voted']
                
                cookie[poll.id] = True

            if user.is_authenticated:
                submission_params['user'] = user
            
            submission = Submission.objects.create(poll=poll, **submission_params)
            for instance in instances:
                instance.submission = submission
                instance.save()
            real_formset.save_m2m()
            messages.success(request, 'Du hast erfolgreich abgestimmt!')
            return redirect('polls:index')
    else:
        real_formset = Formset(queryset=Answer.objects.none(), **formset_params)

    context = {
        'poll': poll,
        'formset': real_formset,
    }
    return render(request, 'polls/polls_vote.html', context)

@login_required
@is_creator
def results(request, token):
    poll = Poll.objects.get(token=token)

    questions = poll.questions.all()

    chart_list = []
    for question in questions:
        if question.type.enable_choices:
            chart_dict = {}
            chart_dict['title'] = question.text
            chart_dict['id'] = question.id
            chart_dict['data'] = []
            chart_dict['labels'] = []
            for choice in question.choices.all():
                chart_dict['labels'].append(choice.text)
                chart_dict['data'].append(choice.answers.count())
            chart_list.append(chart_dict)

    context = {
        'poll': poll,
        'chart_list': chart_list,
    }
    return render(request, 'polls/polls_results.html', context)

@login_required
@is_creator
def get_csv(request, token):
    poll = Poll.objects.get(token=token)

    response = HttpResponse(content_type='text/csv')
    filename = poll.title.replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    
    fieldnames = ['Einsendedatum',]
    for question in poll.questions.all():
        fieldnames.append(question.text)
    
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    
    writer.writeheader()
    for submission in poll.submissions.all():
        write_dict = {}
        write_dict['Einsendedatum'] = submission.submission_date.strftime('%d.%m.%Y %H:%M:%S')
        for answer in submission.answers.all():
            answer_text = ''
            if answer.question.type.enable_choices:
                choice_list = []
                for choice in answer.choices.all():
                    choice_list.append(choice.text)
                answer_text = '; '.join(choice_list)
            else:
                answer_text = answer.value
            write_dict[answer.question.text] = textwrap.fill(answer_text, width=100)
        writer.writerow(write_dict)

    return response

@login_required
@is_creator
def delete(request, token):
    Poll.objects.get(token=token).delete()
    messages.success(request, 'Die Umfrage wurde erfolgreich gelöscht!')
    return redirect('polls:index')

@login_required
@is_creator
def edit(request, token):
    return redirect('polls:index')
    poll = Poll.objects.get(token=token)
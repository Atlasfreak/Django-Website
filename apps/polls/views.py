import csv
import datetime
import textwrap

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .decorators import is_creator
from .forms import *
from .formset import AnswerModelFormset
from .models import *
from .utils import get_poll_from_token, poll_create_csv

# Create your views here.
COOKIE_KEY = "voted_{id}"
SESSION_COOKIE_KEY = "has_voted"


def index_view(request: HttpRequest):
    """
    List all :model:`polls.Poll` for a specific user and all public ones.

    **Context**

    - ``user_polls``
        All the polls associated with one user.
    - ``all_polls``
        All publicly available polls.

    **Template**

    :template:`polls/polls_index.html`
    """
    user = request.user
    user_polls = []
    if user.is_authenticated:
        user_polls = Poll.objects.filter(creator=user).order_by("-start_date")
    all_polls = (
        Poll.objects.are_published().filter(is_public=True).order_by("-start_date")
    )

    context = {
        "user_polls": user_polls,
        "all_polls": all_polls,
    }
    return render(request, "polls/polls_index.html", context)


def construct_choice_formset(
    q_form: forms.Form,
    c_formset: forms.BaseInlineFormSet,
    data=None,
    instance=None,
    queryset=None,
    initial=None,
):
    """Create a choice formset with prefix and additional data."""
    if queryset is None:
        queryset = Choice.objects.none()
    prefix = f"{q_form.prefix}-choice"
    choice_formset = c_formset(
        data,
        prefix=prefix,
        instance=instance,
        queryset=queryset,
        initial=initial,
    )
    return choice_formset


def get_question_type(form: forms.ModelForm):
    if hasattr(form, "cleaned_data") and (
        q_type := form.cleaned_data.get("type", False)
    ):
        return q_type
    return None


def construct_choice_formset_list(
    q_formset: forms.BaseInlineFormSet,
    base_c_formset: forms.BaseInlineFormSet,
    data=None,
    queryset=None,
):
    """Create a list of choice formsets with the correct prefix attached."""
    valid = True
    c_formset_list = []
    for form in q_formset:
        formset_kwargs = {}

        q_type = get_question_type(form)

        if q_type and q_type.enable_choices:
            form_saved = form.save(commit=False)
            formset_kwargs["instance"] = form_saved

        c_formset = construct_choice_formset(
            q_form=form,
            c_formset=base_c_formset,
            data=data,
            queryset=queryset,
            **formset_kwargs,
        )
        valid &= c_formset.is_valid() if formset_kwargs.get("instance", False) else True
        c_formset_list.append(c_formset)

    return (c_formset_list, valid)


def add_extra_params_to_question(q_formset: forms.BaseInlineFormSet, data=None):
    """Add question type parameters to the question."""
    errors = []
    for form in q_formset:
        q_type = get_question_type(form)
        if not q_type:
            continue
        params = q_type.params.all()
        extra_params = {}
        for param in params:
            param_form = get_QuestionTypeParamForm(
                param, replace=form.prefix, data=data
            )
            if param_form.is_valid():
                extra_params.update(param_form.cleaned_data)
            else:
                errors.append(param_form.errors)
        if form.is_valid():
            form.instance.extra_params = extra_params
    return q_formset, errors


@login_required
def create(request: HttpRequest):
    """
    Create a new :model:`polls.Poll`.

    **Context**

    - ``poll_form``
        The form for the :model:`polls.Poll`.
    - ``question_formset``
        The formset for the different :model:`polls.Question`.
    - ``choice_formset_list``
        A list of formsets for the different :model:`polls.Choice`
        every :model:`polls.Question` has one corresponding formset.
    - ``empty_choice_formset``
        A empty :model:`polls.Choice` formset to dynamically add more choices.
    - ``options_deactivated``
        A list of :model:`polls.QuestionType` ids which do not have choices enabled.
    - ``type_param_forms``
        A list of forms to display the input fields for the :model:`polls.QuestionTypeParam`
    - ``type_param_ids_to_forms``
        A dictionary which maps the :model:`polls.QuestionType` ids to their
        :model:`polls.QuestionTypeParam` if there are any. Used in template to display
        respective input fields to user.
    - ``field_ids``
        Dictionary which maps a specific key to a field name. Useful to easily identify fields
        with JavaScript.

    **Template**

    - :template:`polls/polls_create.html` Main Template.
    - :template:`polls/polls_create_complete.html` Template displayed when creation was successful.

    """
    QuestionInlineFormset = inlineformset_factory(
        Poll,
        Question,
        fields=(
            "text",
            "type",
            "required",
            "results_public",
        ),
        max_num=100,
        min_num=1,
        can_delete=False,
        extra=0,
    )

    ChoiceInlineFormset = inlineformset_factory(
        Question,
        Choice,
        fields=("text",),
        max_num=100,
        min_num=1,
        extra=0,
        can_delete=False,
        fk_name="question",
    )
    question_types = QuestionType.objects.all()
    options_deactivated = list(
        question_types.filter(enable_choices=False).values_list("id", flat=True)
    )

    # Create a list of forms for the different parameters to later display the correct inputs

    type_params = QuestionTypeParam.objects.all()
    type_param_forms = []

    for type_param in type_params:
        type_param_form = get_QuestionTypeParamForm(type_param)
        type_param_forms.append(type_param_form)

    choice_formset_list = []

    if request.method == "POST":

        poll_form = PollCreationForm(request.POST, prefix="poll")
        question_formset = QuestionInlineFormset(request.POST, prefix="question")

        if poll_form.is_valid() and question_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator = request.user
            question_formset.instance = poll
            question_formset, param_errors = add_extra_params_to_question(
                question_formset, data=request.POST
            )
            choice_formset_list, choices_valid = construct_choice_formset_list(
                question_formset, ChoiceInlineFormset, data=request.POST
            )

            if choices_valid and not param_errors:
                poll.save()
                question_formset.save()
                for formset in choice_formset_list:
                    if formset.instance.pk:
                        formset.save()
                context = {
                    "poll": poll,
                }
                return render(request, "polls/polls_create_complete.html", context)
            else:
                if param_errors:
                    messages.error(request, "".join(param_errors))
        else:
            choice_formset_list = construct_choice_formset_list(
                question_formset, ChoiceInlineFormset, data=request.POST
            )[0]
    else:
        poll_form = PollCreationForm(prefix="poll")

        question_formset = QuestionInlineFormset(prefix="question")

    # ensure that there is a correct list for choice formsets
    if not choice_formset_list:
        choice_formset_list = construct_choice_formset_list(
            question_formset,
            ChoiceInlineFormset,
        )[0]

    empty_choice_formset = construct_choice_formset(
        question_formset.empty_form, ChoiceInlineFormset
    )

    context = {
        "poll_form": poll_form,
        "question_formset": question_formset,
        "choice_formset_list": choice_formset_list,
        "empty_choice_formset": empty_choice_formset,
        "options_deactivated": options_deactivated,
        "type_param_forms": type_param_forms,
        "type_param_ids_to_forms": QuestionType.objects.get_ids_to_params(),
        "field_ids": {
            "question_text": "text",
            "question_type": "type",
        },
    }
    return render(request, "polls/polls_create.html", context)


def vote(request: HttpRequest, token: str):
    """
    Page to vote for a poll.

    **Context**

    - ``poll``
        The poll to vote for.
    - ``formset``
        The formset with all Answerforms.
    - ``helper``
        Crispy forms helper to better style the forms.

    **Template**

    :template:`polls/polls_vote.html`
    """
    poll, questions = get_poll_from_token(token)
    ip_adress = request.META.get("REMOTE_ADDR")
    cookie_salt = poll.start_date.strftime("%d.%m%m.%Y %H:%M:%S:%f %z %Z %j")

    if not poll.is_published():
        message = "Diese Umfrage ist nicht öffentlich."
        if poll.ended():
            message = "Diese Umfrage ist beendet."
        elif poll.published_in_future():
            message = "Diese Umfrage hat noch nicht gestartet."
        messages.error(request, message)
        return redirect("polls:index")

    session_cookie = request.session.get(SESSION_COOKIE_KEY, False)
    cookie = request.get_signed_cookie(
        COOKIE_KEY.format(id=poll.id), False, salt=cookie_salt
    )
    if session_cookie and cookie:
        has_voted = bool(cookie and session_cookie.get(poll.id, False))
    else:
        has_voted = False

    if not poll.multiple_votes and (
        has_voted or Submission.objects.filter(ip_adress=ip_adress, poll=poll).exists()
    ):
        message = "Du hast für diese Umfrage bereits abgestimmt!"
        messages.error(request, message)
        return redirect("polls:index")

    questions_count = poll.questions.count()

    Formset = formset_factory(
        get_AnswerModelForm,
        formset=AnswerModelFormset,
        extra=0,
        min_num=questions_count,
        max_num=questions_count,
    )
    Formset.model = Answer
    formset_params = {"form_kwargs": {"questions": questions}}

    if request.method == "POST":
        real_formset = Formset(request.POST, **formset_params)

        if real_formset.is_valid():
            instances = real_formset.save(commit=False)
            user = request.user

            submission_params = {}
            cookie_params = {}

            if not poll.multiple_votes:
                submission_params["ip_adress"] = ip_adress

                if not session_cookie:
                    request.session[SESSION_COOKIE_KEY] = {}
                    session_cookie = request.session[SESSION_COOKIE_KEY]

                cookie_params = {"key": COOKIE_KEY.format(id=poll.id), "value": True}
                session_cookie[poll.id] = True

            if user.is_authenticated:
                submission_params["user"] = user

            submission = Submission.objects.create(poll=poll, **submission_params)
            for instance in instances:
                instance.submission = submission
                instance.save()
            real_formset.save_m2m()

            messages.success(request, "Du hast erfolgreich abgestimmt!")

            response = redirect("polls:index")
            if cookie_params:
                expires_time = timezone.now() + datetime.timedelta(366 * 2)
                response.set_signed_cookie(
                    **cookie_params,
                    expires=expires_time,
                    salt=cookie_salt,
                    samesite="lax",
                )
            return response
    else:
        real_formset = Formset(queryset=Answer.objects.none(), **formset_params)

    helper = AnswerFormHelper()
    context = {
        "poll": poll,
        "formset": real_formset,
        "helper": helper,
    }
    return render(request, "polls/polls_vote.html", context)


@login_required
@is_creator
def results(request: HttpRequest, token: str):
    poll, questions = get_poll_from_token(token)

    chart_list = []
    for question in questions:
        if question.type.enable_choices:
            chart_dict = {}
            chart_dict["title"] = question.text
            chart_dict["id"] = question.id
            chart_dict["data"] = []
            chart_dict["labels"] = []
            for choice in question.choices.all():
                chart_dict["labels"].append(choice.text)
                chart_dict["data"].append(choice.answers.count())
            chart_list.append(chart_dict)

    context = {
        "poll": poll,
        "questions": questions,
        "submissions": poll.submissions.all(),
        "chart_list": chart_list,
    }
    return render(request, "polls/polls_results.html", context)


@login_required
@is_creator
def get_csv(request: HttpRequest, token: str):
    poll, questions = get_poll_from_token(token)

    response = HttpResponse(content_type="text/csv")
    filename = poll.title.replace(" ", "_")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'

    response = poll_create_csv(response, poll, questions)

    return response


@login_required
@is_creator
def delete(request: HttpRequest, token: str):
    poll, questions = get_poll_from_token(token)
    poll.delete()
    messages.success(request, "Die Umfrage wurde erfolgreich gelöscht!")
    return redirect("polls:index")


@login_required
@is_creator
def edit(request: HttpRequest, token: str):
    return redirect("polls:index")

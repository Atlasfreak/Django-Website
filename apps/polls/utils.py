import csv
import textwrap

from django.shortcuts import get_object_or_404

from .models import Poll, Question


def get_poll_from_token(token: str):
    """
    get_poll_from_token
    Returns the poll with the specified token.
    Also gets the questions for the poll.

    Args:
        token (str): The token of the poll

    Returns:
        poll: :model:`polls.Poll` Object
        questions: List of :model:`polls.Question` objects for the Poll
    """
    poll = get_object_or_404(Poll.objects.all(), token=token)
    questions = poll.questions.all()
    return poll, questions


def poll_create_csv(file, poll: Poll, questions: Question):
    fieldnames = [
        "Einsendedatum",
    ]
    for question in questions:
        fieldnames.append(question.text)

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for submission in poll.submissions.all():
        write_dict = {}
        write_dict["Einsendedatum"] = submission.submission_date.strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        for answer in submission.answers.all():
            answer_text = ""
            if answer.question.type.enable_choices:
                choice_list = []
                for choice in answer.choices.all():
                    choice_list.append(choice.text)
                answer_text = "; ".join(choice_list)
            else:
                answer_text = answer.value
            write_dict[answer.question.text] = textwrap.fill(answer_text, width=100)
        writer.writerow(write_dict)

    return file

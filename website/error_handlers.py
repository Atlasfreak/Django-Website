from urllib.parse import quote

from django.http.request import HttpRequest
from django.shortcuts import render


def handler404(request: HttpRequest, exception=None):
    exception_repr = None
    try:
        message = exception.args[0]
    except (AttributeError, IndexError):
        pass
    else:
        if isinstance(message, str):
            exception_repr = message

    context = {
        "exception": exception_repr,
        "request_path": quote(request.path),
        "err_title": "Seite nicht gefunden",
    }
    return render(request, context=context, template_name="404.html")


def handler403(request: HttpRequest, exception=None):
    context = {
        "exception": str(exception),
        "err_title": "Fehlende Berechtigung",
    }
    return render(request, context=context, template_name="403.html")


def handler400(request: HttpRequest, exception=None):
    context = {
        "err_title": "Fehlerhafte Anfrage",
    }
    return render(request, context=context, template_name="400.html")


def handler500(request: HttpRequest, exception=None):
    context = {
        "err_title": "Interner Fehler",
    }
    return render(request, context=context, template_name="500.html")

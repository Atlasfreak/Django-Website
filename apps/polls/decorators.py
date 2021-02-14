from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .models import Poll


def is_creator(function=None, error_template_name=None, redirect_url="polls:index"):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            poll = get_object_or_404(Poll.objects.all(), token=kwargs["token"])
            if not poll.creator == request.user:
                message = "Du bist nicht der Ersteller dieser Umfrage"
                if error_template_name:
                    return render(
                        request, error_template_name, context={"message": message}
                    )
                else:
                    messages.error(request, message)
                    return redirect(redirect_url)
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    if function:
        return decorator(function)
    return decorator

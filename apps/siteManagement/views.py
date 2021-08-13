from django.shortcuts import render

from .models import Maintenance

# Create your views here.


def maintenance_mode(request, maintenance_instance: Maintenance):
    context = {
        "expected_end": maintenance_instance.expected_end,
        "err_title": "Wartung",
    }
    return render(request, "503.html", context=context, status=503)

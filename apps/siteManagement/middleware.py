from datetime import timedelta
from django.contrib import messages
from django.contrib.messages.api import get_messages

from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.cache import add_never_cache_headers

from .models import Maintenance
from .views import maintenance_mode


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            maintenance: Maintenance = Maintenance.objects.latest("start_date")
        except:
            maintenance = None
        maintenance_status = maintenance.is_enabled() if maintenance else False
        path = request.path
        admin_path = reverse("admin:index")

        if maintenance_status and not (
            request.user.is_staff or path.startswith(admin_path)
        ):
            response = maintenance_mode(request, maintenance)
            seconds_until_end: int = (
                maintenance.expected_end - timezone.now()
            ).total_seconds()
            response["Retry-After"] = seconds_until_end if seconds_until_end > 0 else 0
            add_never_cache_headers(response)
        else:
            if maintenance_status and request.user.is_staff:
                messages.warning(
                    request, "Die Webseite befindet sich im Wartungsmodus!"
                )
            response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

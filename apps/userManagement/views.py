from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from apps.customUser.forms import CustomUserCreationForm


@sensitive_post_parameters()
def register(request: HttpRequest):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            messages.success(request, f"Account für {username} erstellt!")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "userManagement/register.html", context)


@sensitive_post_parameters()
def change_password(request: HttpRequest):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)
            messages.success(request, "Dein Passwort wurde erfolgreich geändert.")
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)

    context = {"form": form}

    return render(request, "userManagement/change_password.html", context)

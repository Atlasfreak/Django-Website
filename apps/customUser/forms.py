from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .models import SiteUser

UserModel = get_user_model()  # settings.AUTH_USER_MODEL


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    full_name = forms.CharField(
        label=_("Full name"),
        max_length=150,
        required=False,
    )

    class Meta:
        model = SiteUser
        fields = (
            "username",
            "full_name",
            "email",
            "password1",
            "password2",
        )
        field_classes = {"username": UsernameField}


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = "__all__"
        field_classes = {"username": UsernameField}

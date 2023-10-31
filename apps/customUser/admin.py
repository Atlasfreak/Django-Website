from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .models import SiteUser

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class CustomUserAdmin(UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "email",
                    "full_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        "username",
        "email",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    )
    list_filter = ("is_superuser", "is_active", "groups", "date_joined", "last_login")
    search_fields = ("username", "email")
    actions = [
        "activate_action",
        "deactivate_action",
        "make_admin_action",
    ]

    def activate_action(self, request, queryset):
        rows_updated = queryset.update(is_active=True)
        if rows_updated == 1:
            message_part = "1 Benutzer wurde"
        else:
            message_part = f"{rows_updated} Benutzer wurden"
        self.message_user(request, f"{message_part} aktiviert.")

    activate_action.short_description = "Ausgewählte Benutzer aktivieren"

    def deactivate_action(self, request, queryset):
        rows_updated = queryset.update(is_active=False)
        if rows_updated == 1:
            message_part = "1 Benutzer wurde"
        else:
            message_part = f"{rows_updated} Benutzer wurden"
        self.message_user(request, f"{message_part} deaktiviert.")

    deactivate_action.short_description = "Ausgewählte Benutzer deaktivieren"

    def make_admin_action(self, request, queryset):
        rows_updated = queryset.update(is_staff=True, is_superuser=True)
        if rows_updated == 1:
            message_part = "1 Benutzer wurde"
        else:
            message_part = f"{rows_updated} Benutzer wurden"
        message = f"{message_part} zum Admin gemacht."
        self.message_user(request, message)

    make_admin_action.short_description = "Ausgewählte Benutzer zum Admin machen"


admin.site.register(SiteUser, CustomUserAdmin)

"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.main import views as main_views
from apps.userManagement import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.flatpages import views as flat_views
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("", main_views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="userManagement/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="userManagement/logout.html"),
        name="logout",
    ),
    path("register/", user_views.register, name="register"),
    path("polls/", include("apps.polls.urls")),
    path(
        "password/",
        include(
            [
                path(
                    "reset/",
                    include(
                        [
                            path(
                                "",
                                auth_views.PasswordResetView.as_view(
                                    template_name="userManagement/password_reset/reset.html"
                                ),
                                name="password_reset",
                            ),
                            path(
                                "done/",
                                auth_views.PasswordResetDoneView.as_view(
                                    template_name="userManagement/password_reset/done.html"
                                ),
                                name="password_reset_done",
                            ),
                            path(
                                "confirm/<uidb64>/<token>/",
                                auth_views.PasswordResetConfirmView.as_view(
                                    template_name="userManagement/password_reset/confirm.html"
                                ),
                                name="password_reset_confirm",
                            ),
                            path(
                                "complete/",
                                auth_views.PasswordResetCompleteView.as_view(
                                    template_name="userManagement/password_reset/complete.html"
                                ),
                                name="password_reset_complete",
                            ),
                        ]
                    ),
                ),
                path("change/", user_views.change_password, name="password_change"),
            ]
        ),
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("contact/", flat_views.flatpage, {"url": "/contact/"}, name="contact"),
    path("legal/", flat_views.flatpage, {"url": "/contact/"}, name="legal"),
    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = "website.error_handlers.handler404"
handler403 = "website.error_handlers.handler403"
handler400 = "website.error_handlers.handler400"
handler500 = "website.error_handlers.handler500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

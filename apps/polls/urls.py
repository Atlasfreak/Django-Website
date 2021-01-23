from django.urls import include, path

from .views import *

app_name = "polls"
urlpatterns = [
    path("", index_view, name="index"),
    path("create/", create, name="create"),
    path(
        "<token>/",
        include(
            [
                path("vote/", vote, name="vote"),
                path(
                    "results/",
                    include(
                        [
                            path("", results, name="results"),
                            path("csv/", get_csv, name="csv"),
                        ]
                    ),
                ),
                path("edit/", edit, name="edit"),
                path("delete/", delete, name="delete"),
            ]
        ),
    ),
]

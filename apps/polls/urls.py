from django.urls import path, include
from .views import *


app_name = 'polls'
urlpatterns = [
    path('', index_view, name = 'index'),
    path('create/', create, name = 'create'),
    path('<token>/', include([
        path('vote/', vote, name = 'vote'),
        path('results/', results, name = 'results'),
        path('edit/', edit, name = 'edit'),
    ]))
]
from django.db import models
from django.utils import timezone


class PollManager(models.Manager):
    def are_published(self):
        now = timezone.now()
        return self.get_queryset().filter(start_date__lte=now, end_date__gt=now)


class QuestionTypeManager(models.Manager):
    def get_ids_to_params(self):
        queryset = self.get_queryset()
        dict = {}
        for query in queryset:
            dict.update(query.get_id_to_param())
        return dict

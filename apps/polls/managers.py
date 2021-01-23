from django.db import models
from django.utils import timezone


class PollManager(models.Manager):
    def are_published(self):
        now = timezone.now()
        return self.get_queryset().filter(start_date__lte=now, end_date__gt=now)

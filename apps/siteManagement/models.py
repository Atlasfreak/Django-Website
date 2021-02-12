from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Maintenance(models.Model):

    active = models.BooleanField(_("Wartung aktivieren/deaktivieren"))
    start_date = models.DateTimeField(
        _("Start der Warung"), auto_now=False, auto_now_add=True
    )
    expected_end = models.DateTimeField(
        _("Vorraussichtliches Ende"), auto_now=False, auto_now_add=False
    )

    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")

    def switch(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def is_enabled(self):
        return self.active
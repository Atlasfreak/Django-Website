from django.contrib import admin
from django.contrib.sites.models import Site

from .models import *

# Register your models here.
admin.site.site_header = f"{Site.objects.get_current().domain}-Management"


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("active", "start_date", "expected_end")
    list_filter = ("active", "start_date", "expected_end")

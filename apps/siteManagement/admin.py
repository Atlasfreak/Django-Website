from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("active", "start_date", "expected_end")
    list_filter = ("active", "start_date", "expected_end")

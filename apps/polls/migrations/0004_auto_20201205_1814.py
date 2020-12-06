# Generated by Django 3.1.2 on 2020-12-05 17:14

import apps.polls.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20201125_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiontype',
            name='enable_choices',
            field=models.BooleanField(default=False, verbose_name='Optionen verfügbar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questiontype',
            name='form_widget',
            field=models.CharField(default='django.forms.widgets.TextInput', help_text='Vollständiger Pfad zu einem Widget z.B. "django.forms.widget.TextInput".', max_length=255, validators=[apps.polls.validators.FormWidgetValidator()], verbose_name='Django Form Widget Klassen Pfad'),
            preserve_default=False,
        ),
    ]
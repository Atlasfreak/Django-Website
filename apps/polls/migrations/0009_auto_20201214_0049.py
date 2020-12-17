# Generated by Django 3.1.4 on 2020-12-13 23:49

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20201207_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='end_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2020, 12, 13, 23, 19, 3, 702255, tzinfo=utc), message='The date lies in the past.')], verbose_name='Enddatum'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='start_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2020, 12, 13, 23, 19, 3, 702255, tzinfo=utc), message='The date lies in the past.')], verbose_name='Startdatum'),
        ),
    ]
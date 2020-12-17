# Generated by Django 3.1.4 on 2020-12-07 22:45

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20201205_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='end_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2020, 12, 7, 23, 15, 55, 746395), message='The date lies in the past.')], verbose_name='Enddatum'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='start_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2020, 12, 7, 23, 15, 55, 746395), message='The date lies in the past.')], verbose_name='Startdatum'),
        ),
    ]
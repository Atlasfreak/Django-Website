# Generated by Django 3.1.5 on 2021-01-24 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_poll_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='end_date',
            field=models.DateTimeField(verbose_name='Enddatum'),
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-19 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20201219_0329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='choice',
            new_name='choices',
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-14 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_choice_related_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='related_questions',
            field=models.ManyToManyField(blank=True, null=True, to='polls.Question', verbose_name='verknüpfte Fragen'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-14 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20210214_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='related_questions',
            field=models.ManyToManyField(blank=True, to='polls.Question', verbose_name='verknüpfte Fragen'),
        ),
    ]

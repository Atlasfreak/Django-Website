# Generated by Django 3.1.4 on 2020-12-21 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_auto_20201221_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.submission', verbose_name='Einsendung'),
        ),
    ]
# Generated by Django 3.2 on 2021-06-19 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0002_auto_20201217_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
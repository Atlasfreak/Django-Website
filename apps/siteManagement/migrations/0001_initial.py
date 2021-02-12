# Generated by Django 3.1.6 on 2021-02-07 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(verbose_name='Wartung aktivieren/deaktivieren')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Start der Warung')),
                ('expected_end', models.DateTimeField(verbose_name='Vorraussichtliches Ende')),
            ],
            options={
                'verbose_name': 'Maintenance',
                'verbose_name_plural': 'Maintenances',
            },
        ),
    ]

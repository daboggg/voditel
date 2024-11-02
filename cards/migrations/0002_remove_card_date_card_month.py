# Generated by Django 5.1.1 on 2024-11-01 16:06

import month.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='date',
        ),
        migrations.AddField(
            model_name='card',
            name='month',
            field=month.models.MonthField(default=2014, verbose_name='дата начала карты'),
            preserve_default=False,
        ),
    ]
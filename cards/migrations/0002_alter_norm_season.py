# Generated by Django 5.1.1 on 2024-11-18 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='norm',
            name='season',
            field=models.CharField(max_length=20, verbose_name='марка авто и сезон'),
        ),
    ]

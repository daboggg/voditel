# Generated by Django 5.1.1 on 2024-11-03 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_remove_card_date_card_month'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-month']},
        ),
        migrations.AlterField(
            model_name='card',
            name='norm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.norm', verbose_name='норма расхода топлива'),
        ),
        migrations.AlterField(
            model_name='card',
            name='truck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.truck', verbose_name='автомобиль'),
        ),
        migrations.CreateModel(
            name='Departure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('place_of_work', models.CharField(max_length=40)),
                ('probeg_start', models.PositiveIntegerField()),
                ('dictance', models.PositiveIntegerField(blank=True, null=True)),
                ('probeg_end', models.PositiveIntegerField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='cards.card')),
            ],
        ),
    ]

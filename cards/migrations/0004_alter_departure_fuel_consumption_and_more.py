# Generated by Django 5.1.1 on 2024-11-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_truck_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departure',
            name='fuel_consumption',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True, verbose_name='расход топлива (л)'),
        ),
        migrations.AlterField(
            model_name='norm',
            name='liter_per_km',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='пробег (л/км)'),
        ),
        migrations.AlterField(
            model_name='norm',
            name='work_with_pump_liter_per_min',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='работа с насосом (л/мин)'),
        ),
        migrations.AlterField(
            model_name='norm',
            name='work_without_pump_liter_per_min',
            field=models.DecimalField(decimal_places=3, max_digits=4, verbose_name='работа без насоса (л/мин)'),
        ),
        migrations.AlterField(
            model_name='truck',
            name='full_name',
            field=models.CharField(max_length=30, verbose_name='полное название автомобиля'),
        ),
    ]

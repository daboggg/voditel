from django.db import models
from django.urls import reverse

from users.templatetags.common_filters import get_rus_month_year


class Truck(models.Model):
    name = models.CharField(max_length=20, verbose_name="марка автомобиля")
    number = models.CharField(max_length=20, verbose_name="номер автомобиля")

    def __str__(self):
        return f'{self.name} - {self.number}'


class Norm(models.Model):
    season = models.CharField(max_length=20, verbose_name="название сезона и марка авто")
    liter_per_km = models.FloatField(verbose_name="пробег (л/км)")
    work_with_pump_liter_per_min = models.FloatField(verbose_name="работа с насосом (л/мин)")
    work_without_pump_liter_per_min = models.FloatField(verbose_name="работа без насоса (л/мин)")

    def __str__(self):
        return f'{self.season}'


class Card(models.Model):
    month = models.DateField(verbose_name="дата начала карты")
    mileage = models.PositiveIntegerField(verbose_name="пробег на 1 число месяца")
    remaining_fuel = models.FloatField(verbose_name="остаток топлива на 1 число месяца")
    truck = models.ForeignKey(Truck, related_name="cards", on_delete=models.CASCADE, verbose_name='автомобиль')
    norm = models.ForeignKey(Norm, related_name="cards", on_delete=models.CASCADE, verbose_name='норма расхода топлива')

    def __str__(self):
        return f'{self.truck.name} - {get_rus_month_year(self.month)}'

    def get_absolute_url(self):
        return reverse('detail_card', kwargs={'pk': self.id})

    class Meta:
        ordering = ["-month"]


class Departure(models.Model):
    date = models.DateField(verbose_name='дата выезда')
    departure_time = models.TimeField(verbose_name='время выезда')
    return_time = models.TimeField(verbose_name='время возвращения')
    place_of_work = models.CharField(max_length=40, verbose_name='место/цель выезда')
    mileage_start = models.PositiveIntegerField(verbose_name='пробег перед выездом (км)')
    distance = models.PositiveIntegerField(blank=True, null=True, verbose_name='пройдено (км)')
    mileage_end = models.PositiveIntegerField(blank=True, null=True, verbose_name='пробег после выезда (км)')
    with_pump = models.PositiveIntegerField(blank=True, null=True, verbose_name='с насосом (мин)')
    without_pump = models.PositiveIntegerField(blank=True, null=True, verbose_name='без насоса (мин)')
    refueled = models.PositiveIntegerField(blank=True, null=True, verbose_name='заправлено (л)')
    fuel_consumption = models.FloatField(verbose_name='расход топлива (л)')

    card = models.ForeignKey(Card, related_name='departures', on_delete=models.CASCADE, verbose_name='')

    def __str__(self):
        return f'{self.date} - {self.place_of_work}'

    class Meta:
        ordering = ["-date", "-departure_time"]

    # def save(self, *args, **kwargs):
    #     if not self.card.entries.count():
    #         self.probeg_start = self.card.start
    #     else:
    #         entry = Departure.objects.filter(card=self.card).order_by('date').last()
    #         self.probeg_start = entry.probeg_start + 40
    #     super().save(*args, **kwargs)

# todo просмотреть все поля на not null или null

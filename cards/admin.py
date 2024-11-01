from django.contrib import admin

from cards.models import Truck, Norm, Card


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    fields = ['name', 'number']

@admin.register(Norm)
class NormAdmin(admin.ModelAdmin):
    fields = ['season',
              'liter_per_km',
              'work_with_pump_liter_per_min',
              'work_without_pump_liter_per_min', ]

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = ['date', 'mileage', 'remaining_fuel', 'truck', 'norm']

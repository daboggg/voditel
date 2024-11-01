import datetime

from django import forms
from datetime import date

from month.widgets import MonthSelectorWidget

from cards.models import Card, Truck, Norm


class AddCardForm(forms.ModelForm):
    # month = forms.DateField(label="Дата карты",
    #                        initial=datetime.date.today(),
    #                              widget=forms.SelectDateWidget(years=[2024,2025],attrs={'class': 'form-control'}))
    month = forms.DateField(label="Дата карты",
                            widget=MonthSelectorWidget(attrs={'class': 'form-control mt-2 w-75'}),
                            initial=date.today())

    mileage = forms.IntegerField(label="пробег на 1 число месяца",
                                 widget=forms.NumberInput(attrs={'class': 'form-control w-75'}))
    remaining_fuel = forms.FloatField(label='остаток топлива на 1 число месяца',
                                      widget=forms.NumberInput(attrs={'class': 'form-control w-75'}))
    truck = forms.ModelChoiceField(queryset=Truck.objects.all(),
                                   label='автомобиль',
                                   widget=forms.Select(attrs={'class': 'form-control w-75'}))
    norm = forms.ModelChoiceField(queryset=Norm.objects.all(),
                                   label='норма по топливу',
                                   widget=forms.Select(attrs={'class': 'form-control w-75'}))
    class Meta:
        model = Card
        fields = ['month', 'mileage', 'remaining_fuel', 'truck', 'norm']

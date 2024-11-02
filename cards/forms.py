import datetime

from django import forms
from datetime import date

from django.core.exceptions import ValidationError
from month.widgets import MonthSelectorWidget

from cards.models import Card, Truck, Norm


class AddCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.update = kwargs.pop("update", False)
        super().__init__(*args, **kwargs)

    month = forms.DateField(label="дата карты:",
                            widget=MonthSelectorWidget(attrs={'class': 'form-control mt-2 w-75'}),
                            initial=date.today())
    mileage = forms.IntegerField(label="пробег на 1 число месяца:",
                                 widget=forms.NumberInput(attrs={'class': 'form-control w-75'}))
    remaining_fuel = forms.FloatField(label='остаток топлива на 1 число месяца:',
                                      widget=forms.NumberInput(attrs={'class': 'form-control w-75'}))
    truck = forms.ModelChoiceField(queryset=Truck.objects.all(),
                                   label='автомобиль:',
                                   widget=forms.Select(attrs={'class': 'form-control w-75'}))
    norm = forms.ModelChoiceField(queryset=Norm.objects.all(),
                                  label='норма расхода топлива:',
                                  widget=forms.Select(attrs={'class': 'form-control w-75'}))

    class Meta:
        model = Card
        fields = ['month', 'mileage', 'remaining_fuel', 'truck', 'norm']

    def clean(self):
        cd = super().clean()
        month = cd.get('month')
        truck = cd.get('truck')

        if self.update:
            if Card.objects.filter(month=month, truck=truck).exists() \
                    and self.instance.month != month\
                    or Card.objects.filter(month=month, truck=truck).exists()\
                    and self.instance.truck != truck:
                raise ValidationError('Такая карточка уже существует')
        else:
            if Card.objects.filter(month=month, truck=truck).exists():
                raise ValidationError('Такая карточка уже существует')

from datetime import date

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, MonthPickerInput
from django import forms
from django.core.exceptions import ValidationError

from cards.models import Card, Truck, Norm, Departure


class AddCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.update = kwargs.pop("update", False)
        super().__init__(*args, **kwargs)

    month = forms.DateField(label="дата карты:",
                            widget=MonthPickerInput(attrs={'class': 'form-control'}),
                            initial=date.today())
    mileage = forms.IntegerField(label="пробег на 1 число месяца:",
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
    remaining_fuel = forms.FloatField(label='остаток топлива на 1 число месяца:',
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    truck = forms.ModelChoiceField(queryset=Truck.objects.all(),
                                   label='автомобиль:',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    norm = forms.ModelChoiceField(queryset=Norm.objects.all(),
                                  label='норма расхода топлива:',
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Card
        fields = ['month', 'mileage', 'remaining_fuel', 'truck', 'norm']

    def clean(self):
        cd = super().clean()
        month = cd.get('month')
        truck = cd.get('truck')

        # исключает перезапись карточки
        if self.update:
            if Card.objects.filter(month=month, truck=truck).exists() \
                    and self.instance.month != month \
                    or Card.objects.filter(month=month, truck=truck).exists() \
                    and self.instance.truck != truck:
                raise ValidationError('Такая карточка уже существует')
        else:
            if Card.objects.filter(month=month, truck=truck).exists():
                raise ValidationError('Такая карточка уже существует')


class AddDepartureForm(forms.ModelForm):
    date = forms.DateField(
        label='Дата выезда',
        initial=date.today(),
        widget=DatePickerInput(attrs={'class': 'form-control'}))
    time = forms.TimeField(
        label='Время выезда',
        widget=TimePickerInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = '__all__'
        model = Departure

        widgets = {
            'place_of_work': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'mileage_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage_end': forms.NumberInput(attrs={'class': 'form-control'}),
        }
# todo сделать поле card hidden

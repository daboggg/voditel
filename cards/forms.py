from datetime import date, timedelta, datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, MonthPickerInput
from django import forms
from django.core.exceptions import ValidationError

from cards.models import Card, Truck, Norm, Departure


class CardAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.update = kwargs.pop("update", False)
        super().__init__(*args, **kwargs)

    month = forms.DateField(label="дата карты:",
                            widget=MonthPickerInput(attrs={'class': 'form-control'}),
                            initial=date.today())
    mileage = forms.IntegerField(label="пробег на 1 число месяца:",
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
    remaining_fuel = forms.DecimalField(label='остаток топлива на 1 число месяца:',
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
            if Card.objects.filter(month__month=month.month, truck=truck).exists() \
                    and self.instance.month.month != month.month \
                    or Card.objects.filter(month__month=month.month, truck=truck).exists() \
                    and self.instance.truck != truck:
                raise ValidationError('Такая карточка уже существует')
        else:
            if Card.objects.filter(month__month=month.month, truck=truck).exists():
                raise ValidationError('Такая карточка уже существует')


class DepartureAddForm(forms.ModelForm):
    date = forms.DateField(
        label='Дата выезда',
        widget=DatePickerInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['date',
                  'departure_time', 'return_time',
                  'place_of_work', 'mileage_start',
                  'distance', 'mileage_end',
                  'with_pump', 'without_pump',
                  'refueled', 'fuel_consumption',
                  'card', 'user', 'norm'
                  ]
        model = Departure

        widgets = {
            'departure_time': TimePickerInput(attrs={'class': 'form-control'}),
            'return_time': TimePickerInput(attrs={'class': 'form-control'}),
            'place_of_work': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'mileage_start': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'with_pump': forms.NumberInput(attrs={'class': 'form-control'}),
            'without_pump': forms.NumberInput(attrs={'class': 'form-control'}),
            'refueled': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_consumption': forms.HiddenInput(),
            'card': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'norm': forms.HiddenInput()
        }

    def clean(self):
        cd = super().clean()
        prev_departure = self.initial['card'].departures.all().first()

        if prev_departure:
            if prev_departure.departure_time >= prev_departure.return_time:
                prev_dt = datetime.combine(prev_departure.date + timedelta(days=1), prev_departure.return_time)
                dt = datetime.combine(cd['date'], cd['departure_time'])
                if prev_dt > dt:
                    raise ValidationError(
                        f'Дата/время выезда ранее чем закончился предыдущий выезд - {prev_dt.strftime("%d-%m-%Y  %H:%M")}')

        if cd.get('distance') is None and cd.get('mileage_end') is None:
            self.add_error("distance", 'или это заполнить')
            self.add_error("mileage_end", 'или это заполнить')
            raise ValidationError(
                'Одно из указанных полей должно быть заполнено')

        if cd.get('mileage_end') is not None and cd.get('mileage_end') < cd.get("mileage_start"):
            self.add_error('mileage_end', f'должно быть больше или равно {cd.get("mileage_start")}')

        if not cd.get('distance') and not cd.get('with_pump') and not cd.get('without_pump'):
            self.add_error("with_pump", 'или это заполнить')
            self.add_error("without_pump", 'или это заполнить')
            raise ValidationError(
                'Одно из указанных полей должно быть заполнено')

        return cd


class DepartureUpdateForm(forms.ModelForm):
    date = forms.DateField(
        label='Дата выезда',
        widget=DatePickerInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['date',
                  'departure_time', 'return_time',
                  'place_of_work', 'mileage_start',
                  'distance', 'mileage_end',
                  'with_pump', 'without_pump',
                  'refueled',
                  'card', 'norm', 'user', 'fuel_consumption',
                  ]
        model = Departure

        widgets = {
            'departure_time': TimePickerInput(attrs={'class': 'form-control'}),
            'return_time': TimePickerInput(attrs={'class': 'form-control'}),
            'place_of_work': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'mileage_start': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'with_pump': forms.NumberInput(attrs={'class': 'form-control'}),
            'without_pump': forms.NumberInput(attrs={'class': 'form-control'}),
            'refueled': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_consumption': forms.HiddenInput(),
            'card': forms.Select(attrs={'class': 'form-control'}),
            'norm': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(),
        }
        labels = {
            'user': "",
            'fuel_consumption': "",
        }

    def clean(self):
        cd = super().clean()

        if cd.get('distance') is None and cd.get('mileage_end') is None:
            self.add_error("distance", 'или это заполнить')
            self.add_error("mileage_end", 'или это заполнить')
            raise ValidationError(
                'Одно из указанных полей должно быть заполнено')

        if cd.get('mileage_end') is not None and cd.get('mileage_end') < cd.get("mileage_start"):
            self.add_error('mileage_end', f'должно быть больше или равно {cd.get("mileage_start")}')

        if not cd.get('distance') and not cd.get('with_pump') and not cd.get('without_pump'):
            self.add_error("with_pump", 'или это заполнить')
            self.add_error("without_pump", 'или это заполнить')
            raise ValidationError(
                'Одно из указанных полей должно быть заполнено')

        return cd


class ShortReportEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

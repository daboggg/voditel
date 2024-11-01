from datetime import date

from django import template

register = template.Library()


@register.filter
def alert_class(value):
    alerts = {
        'debug': 'secondary',
        'error': 'danger'
    }
    if value in alerts:
        return alerts.get(value)
    return value

@register.filter
def get_rus_month_year(dt: date) -> str:
    months = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
    ]

    return f"{months[dt.month-1]} {dt.year}"
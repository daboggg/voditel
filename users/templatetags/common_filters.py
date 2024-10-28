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

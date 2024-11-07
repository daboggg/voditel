from itertools import groupby
from operator import attrgetter
from django.db.models.functions import TruncDate

from cards.models import Departure

queryset = Departure.objects.annotate(
    created_at_date=TruncDate('date'),
).order_by('date')
groupedset = groupby(queryset, attrgetter('created_at_date'))
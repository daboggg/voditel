from _decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from cards.forms import CardAddForm, DepartureAddForm, DepartureUpdateForm
from cards.models import Card, Departure, Norm
from mixins import ErrorMessageMixin


def home(request):
    return render(request, 'cards/home.html', {'title': 'Главная страница'})


class CardList(LoginRequiredMixin, ListView):
    model = Card
    template_name = "cards/card_list.html"
    extra_context = {'title': 'Список карточек'}
    context_object_name = 'cards'
    paginate_by = 7


class CardAdd(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    form_class = CardAddForm
    template_name = 'cards/card_add.html'
    extra_context = {'title': 'Добавить карточку'}
    # success_url = reverse_lazy('card-list')
    success_message = "Карточка создана"
    error_message = 'Ошибка!'


class CardDetail(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'cards/card_detail.html'
    context_object_name = 'card'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'{self.object}'
        res = dict()

        # актуальный остаток топлива в баках
        fuel_in_tanks = self.object.departures.aggregate(
            fuel_in_tanks=F('card__remaining_fuel') -
                          Sum('fuel_consumption') +
                          Sum('refueled', default=0))\
            .get('fuel_in_tanks')
        ctx['fuel_in_tanks'] = fuel_in_tanks.normalize() if fuel_in_tanks else self.object.remaining_fuel

        # для пагинации выездов
        for item in self.object.departures.all():
            if item.date not in res:
                res[item.date] = []
            res.get(item.date).append(item)
        paginator = Paginator(list(res.values()), 7)
        page_obj = paginator.page(int(self.request.GET.get('page', 1)))
        ctx['paginator'] = paginator
        ctx['page_obj'] = page_obj
        ctx['departures'] = page_obj.object_list

        return ctx


class CardUpdate(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Card
    form_class = CardAddForm
    success_message = "Данные изменены"
    error_message = "Ошибка!"
    template_name = 'cards/card_add.html'
    extra_context = {'title': 'Изменить карточку'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['update'] = True
        return kwargs


class CardDelete(LoginRequiredMixin, DeleteView):
    model = Card
    success_url = reverse_lazy("card_list")


class DepartureAdd(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    form_class = DepartureAddForm
    template_name = 'cards/departure_add.html'
    success_message = "Выезд добавлен"
    error_message = 'Ошибка!'

    def get_success_url(self):
        return reverse_lazy('card_detail', kwargs={'pk': self.card.id})

    def setup(self, request, *args, **kwargs):
        self.card = get_object_or_404(Card, pk=kwargs['pk'])
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Добавить выезд'
        ctx['card'] = self.card
        return ctx

    def get_initial(self):
        initial = super().get_initial()
        initial['card'] = self.card
        initial['user'] = self.request.user
        initial['norm'] = self.card.norm
        departures = self.card.departures.all()

        if not departures:
            initial['mileage_start'] = self.card.mileage
        else:
            initial['mileage_start'] = departures.first().mileage_end
        return initial


class DepartureDetail(LoginRequiredMixin, DetailView):
    model = Departure
    template_name = 'cards/departure_detail.html'
    context_object_name = 'departure'


class DepartureDelete(LoginRequiredMixin, DeleteView):
    model = Departure

    def get_success_url(self):
        return reverse_lazy('card_detail', kwargs={'pk': self.object.card.pk})


class DepartureUpdate(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Departure
    form_class = DepartureUpdateForm
    success_message = "Данные изменены"
    error_message = "Ошибка!"
    template_name = 'cards/departure_edit.html'
    extra_context = {'title': 'Изменить данные'}

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['update'] = True
    #     return kwargs


class NormList(LoginRequiredMixin, ListView):
    model = Norm
    template_name = "cards/norm_list.html"
    extra_context = {'title': 'Нормы'}
    context_object_name = 'norms'










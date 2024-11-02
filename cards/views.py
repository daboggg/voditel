from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from cards.forms import AddCardForm
from cards.models import Card
from mixins import ErrorMessageMixin


def home(request):
    return render(request, 'cards/home.html', {'title': 'Главная страница'})


class ListCard(LoginRequiredMixin, ListView):
    model = Card
    template_name = "cards/list_card.html"
    extra_context = {'title': 'Список карточек'}
    context_object_name = 'cards'
    paginate_by = 7


class AddCard(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    form_class = AddCardForm
    template_name = 'cards/add_card.html'
    extra_context = {'title': 'Добавить карточку'}
    # success_url = reverse_lazy('list_card')
    success_message = "Карточка создана"
    error_message = 'Ошибка!'


class DetailCard(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'cards/detail_card.html'
    context_object_name = 'card'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'{self.object}'
        return ctx


class UpdateCard(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Card
    form_class = AddCardForm
    success_message = "Данные изменены"
    error_message = "Ошибка!"
    template_name = 'cards/add_card.html'
    extra_context = {'title': 'Изменить карточку'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['update'] = True
        return kwargs








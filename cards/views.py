from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from cards.forms import AddCardForm
from cards.models import Card


def home(request):
    return render(request, 'cards/home.html', {'title':'Главная страница'})


class ListCard(LoginRequiredMixin, ListView):
    model = Card
    template_name = "cards/list_card.html"
    extra_context = {'title': 'Список карточек'}
    context_object_name = 'cards'
    paginate_by = 7


class AddCard(LoginRequiredMixin, CreateView):
    form_class = AddCardForm
    template_name = 'cards/add_card.html'
    extra_context = {'title': 'Добавить карточку'}
    # success_url = reverse_lazy('list_card')


class DetailCard(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'cards/detail_card.html'
    context_object_name = 'card'
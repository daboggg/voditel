from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from weasyprint import HTML, CSS

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
                          Sum('refueled', default=0)) \
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

        if 'eto' in self.request.GET:
            initial['departure_time'] = '08:00:00'
            initial['return_time'] = '08:30:00'
            initial['place_of_work'] = 'ЕТО'
            initial['distance'] = 0
            initial['without_pump'] = 5

        if 'dozor' in self.request.GET:
            initial['departure_time'] = '21:00:00'
            initial['return_time'] = '22:00:00'
            initial['place_of_work'] = 'Целевой дозор'
            initial['distance'] = 4
            initial['without_pump'] = 30

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


class NormAdd(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = Norm
    template_name = 'cards/norm_add.html'
    extra_context = {'title': 'Добавить норму'}
    success_url = reverse_lazy('norm_list')
    success_message = "Норма создана"
    error_message = 'Ошибка!'
    fields = '__all__'


class NormDelete(LoginRequiredMixin, DeleteView):
    model = Norm
    success_url = reverse_lazy('norm_list')


class NormUpdate(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Norm
    fields = '__all__'
    success_url = reverse_lazy('norm_list')
    success_message = "Данные изменены"
    error_message = "Ошибка!"
    template_name = 'cards/norm_add.html'
    extra_context = {'title': 'Изменить норму'}


class ReportDetail(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'cards/report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Отчет {self.object}'

        report_data = self.object.departures.aggregate(
            total_distance=Sum('distance', default=0),
            total_mileage_consumption=Sum('distance', default=0) * self.object.norm.liter_per_km,
            total_time_with_pump=Sum('with_pump', default=0),
            total_with_pump_consumption=Sum('with_pump', default=0) * self.object.norm.work_with_pump_liter_per_min,
            total_time_without_pump=Sum('without_pump', default=0),
            total_without_pump_consumption=Sum('without_pump',
                                               default=0) * self.object.norm.work_without_pump_liter_per_min,
            total_refueled=Sum('refueled', default=0),
            total_fuel_consumption=F('total_mileage_consumption') + F('total_with_pump_consumption') + F(
                'total_without_pump_consumption'),
            remaining_fuel_end_month=self.object.remaining_fuel + F('total_refueled') - F('total_fuel_consumption')
        )
        ctx['report_data'] = report_data
        return ctx


# def getpdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="file.pdf"'
#     p = canvas.Canvas(response)
#     p.setFont("Times-Roman", 55)
#     p.drawString(100, 700, "Hello pidar.")
#     p.showPage()
#     p.save()
#     return response


def convert_html_to_pdf_stream(template: str, context: dict) -> BytesIO:
    html_content = render_to_string(template, context)
    memory_buffer = BytesIO()
    pdf = HTML(string=html_content).write_pdf(target=memory_buffer, stylesheets=[CSS(string='@page {size: landscape}')])

    return memory_buffer


def get_short_report_pdf(request):

    pdf_stream = convert_html_to_pdf_stream('cards/short_report_pdf.html', {'title': 'ЖЖЖЖ'})
    response = HttpResponse(pdf_stream.getvalue(), content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="your_file.pdf"'
    return response


def get_full_report_pdf(request):
    pdf_stream = convert_html_to_pdf_stream('cards/full_report_pdf.html', {'title': 'ЖЖЖЖ'})
    response = HttpResponse(pdf_stream.getvalue(), content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="your_file.pdf"'
    return response

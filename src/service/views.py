import string, random
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView
)
from itertools import chain
from .models import Service
from .forms import ServiceForm
from django.db.models import Sum
from django.http import JsonResponse

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service/service_list.html'
    context_object_name = 'object'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, query=None):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            results = Service.objects.search(query)
            queryset_chain = chain(results)     
            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                reverse=True)
            self.count = len(qs)
            return qs
        return Service.objects.all()

class ServiceView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service/service_detail.html'
    context_object_name = 'object'
    # paginate_by = 20
    slug = None

    def get_object(self):
        instance = get_object_or_404(Service, slug=self.kwargs.get('slug'))
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # payment = Payment.objects.get(service=self.get_object())
        # context['commission'] = Commission.objects.filter(service=self.get_object(), active=True).aggregate(Sum('amount'))['amount__sum']
        # context['investment'] = Investment.objects.filter(service=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        # context['balance'] = payment.balance
        # context['withdraw'] = Withdraw.objects.filter(service=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        return context

class ServiceCreateView(CreateView):
    form_class = ServiceForm
    template_name = 'service/service_form.html'

    def get_success_url(self):
        return reverse('service:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Create Service'
        return context

    def form_valid(self, form):
        service = form.save(commit=False)
        messages.success(self.request, "Successfully Created")
        service.save()
        return super(ServiceCreateView, self).form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_form.html'

    def get_success_url(self):
        return reverse('service:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Update Service'
        return context

    def form_valid(self, form):
        service = form.save(commit=False)
        messages.success(self.request, "Successfully Updated")
        service.save()
        return super(ServiceUpdateView, self).form_valid(form)

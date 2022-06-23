from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import BillingProfile, Charge

class BillingListView(LoginRequiredMixin, ListView):
    model = BillingProfile
    template_name = 'billing/billing_list.html'
    context_object_name = 'object'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            results = BillingProfile.objects.search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        return BillingProfile.objects.all()

class ChargeListView(LoginRequiredMixin, ListView):
    model = Charge
    template_name = 'billing/charge_list.html'
    context_object_name = 'object'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            if self.request.user.staff:
                results = Charge.objects.search(query)
            elif self.request.user.business:
                results = Charge.objects.filter(vendor=self.request.user.get_acc()).search(query)
            else:
                results = Charge.objects.filter(client=self.request.user.get_acc()).search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        if self.request.user.staff:
            return Charge.objects.all()
        elif self.request.user.business:
            billing = BillingProfile.objects.filter(vendor=self.request.user.get_acc()).first()
            return Charge.objects.filter(billing=billing)
        else:
            billing = BillingProfile.objects.filter(client=self.request.user.get_acc()).first()
            return Charge.objects.filter(billing=billing)

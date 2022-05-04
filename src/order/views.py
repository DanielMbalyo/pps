from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render

from src.billing.models import BillingProfile
from .models import Order

class BillingListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_bill.html'

    def get_queryset(self):
        return Order.objects.filter_by_package(self.request)

    def get_context_data(self, **kwargs):
        context = super(BillingListView, self).get_context_data(**kwargs)
        return context

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter_by_instance(self.request)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):

    def get_object(self, *args, **kwargs):
        qs = Order.objects.by_request(self.request).filter(
            order_id = self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        raise Http404
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        return context

class VerifyOwnership(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404
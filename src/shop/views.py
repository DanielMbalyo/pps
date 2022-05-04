import string, random
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView
)
from itertools import chain
from .models import Shop
from .forms import ShopForm
from django.db.models import Sum
from django.http import JsonResponse

class ShopListView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'shop/shop_list.html'
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
            results = Shop.objects.search(query)
            queryset_chain = chain(results)     
            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                reverse=True)
            self.count = len(qs)
            return qs
        return Shop.objects.all()

class ShopView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'shop/shop_detail.html'
    context_object_name = 'object'
    # paginate_by = 20
    slug = None

    def get_object(self):
        instance = get_object_or_404(Shop, slug=self.kwargs.get('slug'))
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # payment = Payment.objects.get(shop=self.get_object())
        # context['commission'] = Commission.objects.filter(shop=self.get_object(), active=True).aggregate(Sum('amount'))['amount__sum']
        # context['investment'] = Investment.objects.filter(shop=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        # context['balance'] = payment.balance
        # context['withdraw'] = Withdraw.objects.filter(shop=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        return context

class ShopCreateView(CreateView):
    form_class = ShopForm
    template_name = 'shop/shop_form.html'

    def get_success_url(self):
        return reverse('shop:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Create Shop'
        return context

    def form_valid(self, form):
        shop = form.save(commit=False)
        shop.account = self.request.user.get_acc()
        messages.success(self.request, "Successfully Created")
        shop.save()
        return super(ShopCreateView, self).form_valid(form)

class ShopUpdateView(LoginRequiredMixin, UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = 'shop/shop_form.html'

    def get_success_url(self):
        return reverse('shop:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Update Shop'
        return context

    def form_valid(self, form):
        shop = form.save(commit=False)
        messages.success(self.request, "Successfully Updated")
        shop.save()
        return super(ShopUpdateView, self).form_valid(form)

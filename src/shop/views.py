import string, random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView, TemplateView
)
from itertools import chain
from .models import Shop, Vendor
from .forms import ShopForm, VendorForm
from django.db.models import Sum
from django.http import JsonResponse

from src.product.models import UserProduct

User = get_user_model()

class ShopPolicyView(TemplateView):
    template_name = 'shop/policy.html'

class ShopListView(LoginRequiredMixin, ListView):
    model = Vendor
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
            results = Vendor.objects.search(query)
            queryset_chain = chain(results)     
            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                reverse=True)
            self.count = len(qs)
            return qs
        return Vendor.objects.all()

class ShopFrontView(ListView):
    model = UserProduct
    template_name = 'shop/shop_front.html'
    context_object_name = 'object'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        shop = Shop.objects.filter(slug=self.kwargs.get('slug')).first()
        context['name'] = shop.name
        context['slug'] = self.kwargs.get('slug')
        print(self.kwargs.get('slug'))
        context['products'] = UserProduct.objects.filter(shop=shop)
        return context

    def get_queryset(self, query=None):
        request = self.request
        query = request.GET.get('q', None)
        shop = Shop.objects.filter(slug=self.kwargs.get('slug')).first()
        if query is not None:
            results = UserProduct.objects.filter(shop=shop).search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        return UserProduct.objects.filter(shop=shop)

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
        vendor = Vendor.objects.filter(slug=self.kwargs.get('slug')).first()
        shop = Shop.objects.filter(owner=vendor).first()
        self.request.session['vendor'] = None
        context['vendor'] = vendor
        context['shop'] = shop
        context['product'] = UserProduct.objects.filter(shop=shop).count()
        context['products'] = UserProduct.objects.filter(shop=shop)
        # payment = Payment.objects.get(shop=self.get_object())
        # context['commission'] = Commission.objects.filter(shop=self.get_object(), active=True).aggregate(Sum('amount'))['amount__sum']
        # context['investment'] = Investment.objects.filter(shop=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        # context['balance'] = payment.balance
        # context['withdraw'] = Withdraw.objects.filter(shop=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        return context

class VendorCreateView(CreateView):
    form_class = VendorForm
    template_name = 'shop/form.html'

    def get_success_url(self):
        return reverse('shop:create')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Create Shop'
        return context

    def form_valid(self, form):
        email = self.request.session.get('email')
        if email:
            password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
            vendor = form.save(commit=False)
            vendor.account = User.objects.create(email=email, password=password, vendor=True)
            vendor.save()
            self.request.session['email'] = None
            self.request.session['type'] = None
            self.request.session['vendor'] = vendor.id
            messages.success(self.request, "Successfully Created")
        else:
            messages.success(self.request, "Invalid Mail")
        return super(VendorCreateView, self).form_valid(form)

class ShopCreateView(CreateView):
    form_class = ShopForm
    template_name = 'shop/form.html'

    def get_success_url(self):
        return reverse('shop:summary')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Create Shop'
        return context

    def form_valid(self, form):
        id = self.request.session.get('vendor')
        shop = form.save(commit=False)
        shop.owner = Vendor.objects.filter(id=id).first()
        shop.save()
        messages.success(self.request, "Successfully Created")
        return super(ShopCreateView, self).form_valid(form)

class ShopSummaryView(ListView):
    template_name = 'shop/summary.html'
    model = Shop

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        id = self.request.session.get('vendor', None)
        vendor = Vendor.objects.filter(id=id).first()
        shop = Shop.objects.filter(owner=vendor).first()
        self.request.session['vendor'] = None
        context['vendor'] = vendor
        context['shop'] = shop
        return context

class ShopCompleteView(TemplateView):
    template_name = 'shop/summary.html'

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

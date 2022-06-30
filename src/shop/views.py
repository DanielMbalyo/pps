import string, random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView, TemplateView, FormView
)
from itertools import chain
from .models import Shop, Vendor
from .forms import ShopForm, VendorForm, InquiryForm
from django.db.models import Sum
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from src.product.models import UserProduct
from src.cart.models import Cart, CartItem

from src.order.models import Order
from src.billing.models import BillingProfile, Charge

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
        vendor = Vendor.objects.filter(slug=self.kwargs.get('slug')).first()
        cart = Cart.objects.filter(vendor=vendor).first()
        cart_item = CartItem.objects.filter(cart=cart)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['cart'] = cart
        context['items'] = cart_item
        return context

    def get_queryset(self, query=None):
        request = self.request
        query = request.GET.get('q', None)
        vendor = Vendor.objects.filter(slug=self.kwargs.get('slug')).first()
        if query is not None:
            results = UserProduct.objects.filter(vendor=vendor).search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        return UserProduct.objects.filter(vendor=vendor)

class ShopProductView(ListView):
    model = UserProduct
    template_name = 'shop/shop_product.html'
    context_object_name = 'products'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        vendor = Vendor.objects.filter(slug=self.kwargs.get('slug')).first()
        context['vendor'] = vendor
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, query=None):
        request = self.request
        query = request.GET.get('q', None)
        vendor = Vendor.objects.filter(slug=self.kwargs.get('slug')).first()
        if query is not None:
            results = UserProduct.objects.filter(vendor=vendor).search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        return UserProduct.objects.filter(vendor=vendor)

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
        billing = BillingProfile.objects.filter(vendor=vendor).first()
        context['vendor'] = vendor
        context['shop'] = Shop.objects.filter(owner=vendor).first()
        context['product'] = UserProduct.objects.filter(vendor=vendor).count()
        context['orders'] = Order.objects.filter(vendor=vendor).count()
        context['billing'] = billing
        context['charges'] = Charge.objects.filter(billing=billing).count()
        return context

class VendorCreateView(CreateView):
    form_class = VendorForm
    template_name = 'shop/form.html'

    def get_success_url(self):
        return reverse('shop:create')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Vendor Details'
        context['message'] = 'Details about you, a person who provides services you offer to the customers'
        return context

    def form_valid(self, form):
        email = self.request.session.get('email')
        if email:
            password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
            vendor = form.save(commit=False)
            vendor.account = User.objects.create(email=email, password=password, business=True)
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
        context['title'] = 'Business Details'
        context['message'] = 'Details that tells us more about the services you offer to the customers'
        return context

    def form_valid(self, form):
        id = self.request.session.get('vendor')
        shop = form.save(commit=False)
        shop.owner = Vendor.objects.filter(id=id).first()
        shop.save()
        messages.success(self.request, "Successfully Created")
        return super(ShopCreateView, self).form_valid(form)

class ShopInquireView(FormView):
    form_class = InquiryForm
    template_name = 'shop/shop_form.html'

    def get_success_url(self):
        return reverse('shop:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Inqure Form'
        return context

    def form_valid(self, form):
        instance = get_object_or_404(Vendor, slug=self.kwargs.get('slug'))
        inquiry = self.request.POST.get("inqury")
        context = {'reason': inquiry,}
        txt_ = get_template("account/emails/reply.txt").render(context)
        html_ = get_template("account/emails/reply.html").render(context)
        sent_mail = send_mail(
            'Futher Inquiry', txt_, settings.DEFAULT_FROM_EMAIL,
            [instance.account.email], html_message=html_, fail_silently=False,)
        messages.success(self.request, "Email Successfully Sent")
        return super(ShopInquireView, self).form_valid(form)

class ShopRejectView(FormView):
    form_class = InquiryForm
    template_name = 'shop/shop_form.html'

    def get_success_url(self):
        return reverse('shop:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Reject Form'
        return context

    def form_valid(self, form):
        instance = get_object_or_404(Vendor, slug=self.kwargs.get('slug'))
        inquiry = self.request.POST.get("inqury")
        context = {'reason': inquiry,}
        txt_ = get_template("account/emails/reply.txt").render(context)
        html_ = get_template("account/emails/reply.html").render(context)
        sent_mail = send_mail(
            'Request Rejection', txt_, settings.DEFAULT_FROM_EMAIL,
            [instance.account.email], html_message=html_, fail_silently=False,)
        messages.success(self.request, "Email Successfully Sent")
        return super(ShopRejectView, self).form_valid(form)

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

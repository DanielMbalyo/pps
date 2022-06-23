import string, random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView, TemplateView
)
from itertools import chain
from .models import Client, Finance
from .forms import ClientForm, FinanceForm, InquiryForm
from django.db.models import Sum
from django.core.mail import send_mail
from django.template.loader import get_template

from src.order.models import Order
from src.billing.models import BillingProfile, Charge

from src.shop.models import Shop

User = get_user_model()

class ClientPolicyView(TemplateView):
    template_name = 'client/policy.html'

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_list.html'
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
            results = Client.objects.search(query)
            queryset_chain = chain(results)     
            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                reverse=True)
            self.count = len(qs)
            return qs
        return Client.objects.all()

class ClientView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_detail.html'
    context_object_name = 'object'
    slug = None

    def get_object(self):
        instance = get_object_or_404(Client, slug=self.kwargs.get('slug'))
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        client = Client.objects.filter(slug=self.kwargs.get('slug')).first()
        billing = BillingProfile.objects.filter(client=client).first()
        context['client'] = client
        context['finance'] = Finance.objects.filter(client=client).first()
        context['orders'] = Order.objects.filter(client=client).count()
        context['billing'] = billing
        context['charges'] = Charge.objects.filter(billing=billing).count()
        return context

class ClientCreateView(CreateView):
    form_class = ClientForm
    template_name = 'client/form.html'

    def get_success_url(self):
        return reverse('client:finance')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Personal Details'
        context['message'] = 'Details about you, a person who will receive services from our system.'
        return context    

    def form_valid(self, form):
        email = self.request.session.get('email')
        if email:
            password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
            client = form.save(commit=False)
            client.account = User.objects.create_user(email=email, password=password)
            client.save()
            self.request.session['email'] = None
            self.request.session['type'] = None
            self.request.session['client'] = client.id
            messages.success(self.request, "Successfully Created")
        else:
            messages.success(self.request, "Invalid Mail")
        return super(ClientCreateView, self).form_valid(form)

class ClientFinanceView(CreateView):
    form_class = FinanceForm
    template_name = 'client/form.html'

    def get_success_url(self):
        return reverse('client:summary')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Financial Details'
        context['message'] = 'Details that tells us more about the your eligibility to our services.'
        return context

    def form_valid(self, form):
        id = self.request.session.get('client')
        client = form.save(commit=False)
        client.client = Client.objects.filter(id=id).first()
        client.save()
        messages.success(self.request, "Successfully Created")
        return super(ClientFinanceView, self).form_valid(form)

class ClientInquireView(CreateView):
    form_class = InquiryForm
    template_name = 'client/client_form.html'

    def get_success_url(self):
        return reverse('client:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Inqure Form'
        return context

    def form_valid(self, form):
        instance = get_object_or_404(Client, slug=self.kwargs.get('slug'))
        inqury = self.request.POST.get("inqury")
        context = {'reason': inquiry,}
        txt_ = get_template("account/emails/reply.txt").render(context)
        html_ = get_template("account/emails/reply.html").render(context)
        sent_mail = send_mail(
            'Futher Inquiry', txt_, settings.DEFAULT_FROM_EMAIL,
            [instance.account.email], html_message=html_, fail_silently=False,)
        messages.success(self.request, "Email Successfully Sent")
        return super(ClientInquireView, self).form_valid(form)

class ClientRejectView(CreateView):
    form_class = InquiryForm
    template_name = 'client/client_form.html'

    def get_success_url(self):
        return reverse('client:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Reject Form'
        return context

    def form_valid(self, form):
        instance = get_object_or_404(Client, slug=self.kwargs.get('slug'))
        inqury = self.request.POST.get("inqury")
        context = {'reason': inquiry,}
        txt_ = get_template("account/emails/reply.txt").render(context)
        html_ = get_template("account/emails/reply.html").render(context)
        sent_mail = send_mail(
            'Request Rejection', txt_, settings.DEFAULT_FROM_EMAIL,
            [instance.account.email], html_message=html_, fail_silently=False,)
        messages.success(self.request, "Email Successfully Sent")
        return super(ClientRejectView, self).form_valid(form)

class ClientSummaryView(ListView):
    template_name = 'client/summary.html'
    model = Client

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        id = self.request.session.get('client', None)
        client = Client.objects.filter(id=id).first()
        finance = Finance.objects.filter(client=client).first()
        self.request.session['client'] = None
        context['client'] = client
        context['finance'] = finance
        return context

class ClientCompleteView(TemplateView):
    template_name = 'client/summary.html'

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'

    def get_success_url(self):
        return reverse('client:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Update Client'
        return context

    def form_valid(self, form):
        client = form.save(commit=False)
        messages.success(self.request, "Successfully Updated")
        client.save()
        return super(ClientUpdateView, self).form_valid(form)

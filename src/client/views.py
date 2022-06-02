import string, random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView, TemplateView
)
from itertools import chain
from .models import Client
from .forms import ClientForm
from django.db.models import Sum

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
    # paginate_by = 20
    slug = None

    def get_object(self):
        instance = get_object_or_404(Client, slug=self.kwargs.get('slug'))
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['investment'] = Investment.objects.filter(client=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        # context['balance'] = payment.balance
        # context['withdraw'] = Withdraw.objects.filter(client=self.get_object()).aggregate(Sum('amount'))['amount__sum']
        return context

class ClientCreateView(CreateView):
    form_class = ClientForm
    template_name = 'client/form.html'

    def get_success_url(self):
        return reverse('account:login')

    def form_valid(self, form):
        email = self.request.session.get('email')
        password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
        client = form.save(commit=False)
        client.account = User.objects.create_user(email=email, password=password)
        client.save()
        self.request.session['email'] = ''
        self.request.session['type'] = ''
        messages.success(self.request, "Successfully Created")
        return super(ClientCreateView, self).form_valid(form)

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

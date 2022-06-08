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
from .forms import ClientForm, FinanceForm
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
        return reverse('client:finance')

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
            print(client.id)
            messages.success(self.request, "Successfully Created")
        else:
            messages.success(self.request, "Invalid Mail")
        return super(ClientCreateView, self).form_valid(form)

class ClientFinanceView(CreateView):
    form_class = FinanceForm
    template_name = 'client/form.html'

    def get_success_url(self):
        return reverse('client:summary')

    def form_valid(self, form):
        id = self.request.session.get('client')
        client = form.save(commit=False)
        client.client = Client.objects.filter(id=id).first()
        client.save()
        self.request.session['client'] = None
        messages.success(self.request, "Successfully Created")
        return super(ClientFinanceView, self).form_valid(form)

class ClientSummaryView(TemplateView):
    template_name = 'client/summary.html'

class ClientCompleteView(TemplateView):
    template_name = 'client/summary.html'

    def get(self, request):
        id = self.request.session.get('client', None)
        print(id)
        if not id:
            return redirect("account:login")
        client = Client.objects.filter(id=id).first()
        finance = Finance.objects.filter(client=client)
        context = {
            "client": client,
            "finance": finance,
        }
        return render(self.request, "client/summary.html", context)

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

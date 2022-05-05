import string, random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView
)
from itertools import chain
from .models import Manager
from django.db.models import Sum
from .forms import ManagerForm

from src.client.models import Client
from src.shop.models import Shop
from src.product.models import Product

User = get_user_model()

class ManagerListView(LoginRequiredMixin, ListView):
    model = Manager
    template_name = 'manager/manager_list.html'
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
            results = Manager.objects.search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                reverse=True)
            self.count = len(qs)
            return qs
        return Manager.objects.all()

class ManagerView(LoginRequiredMixin, DetailView):
    model = Manager
    template_name = 'manager/manager_detail.html'
    context_object_name = 'object'
    slug = None

    def get_object(self):
        instance = get_object_or_404(Manager, slug=self.kwargs.get('slug'))
        return instance

    def get_context_data(self, *args, **kwargs):
        count = 0
        context = super().get_context_data(*args, **kwargs)
        clients = Client.objects.all()
        context['products'] = Product.objects.all().count()
        context['clients'] = Client.objects.all().count()
        context['shops'] = Shop.objects.all().count()
        # context['investments'] = Investment.objects.aggregate(Sum('amount'))['amount__sum']
        return context

class ManagerCreateView(LoginRequiredMixin, CreateView):
    form_class = ManagerForm
    template_name = 'manager/manager_form.html'

    def get_success_url(self):
        return reverse('manager:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Create Admin'
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
        manager = form.save(commit=False)
        manager.account = User.objects.create_user(email=email, password=password, is_staff=True)
        messages.success(self.request, "Successfully Created")
        manager.save()
        return super(ManagerCreateView, self).form_valid(form)

class ManagerUpdateView(LoginRequiredMixin, UpdateView):
    model = Manager
    form_class = ManagerForm
    template_name = 'manager/manager_form.html'

    def get_success_url(self):
        return reverse('manager:list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Update Admin'
        return context

    def form_valid(self, form):
        manager = form.save(commit=False)
        messages.success(self.request, "Successfully Updated")
        manager.save()
        return super(ManagerUpdateView, self).form_valid(form)

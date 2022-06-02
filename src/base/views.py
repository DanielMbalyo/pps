from itertools import chain
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import redirect, render, reverse, get_object_or_404

from src.shop.models import Shop

class LandingView(TemplateView):
    template_name = 'base/landing.html'

class HomeView(ListView):
    model = Shop
    template_name = 'base/home.html'
    context_object_name = 'shops'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['map_api_key'] = settings.MAP_API_KEY
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

    # def get_queryset(self, query=None):
    #     request = self.request
    #     query = request.GET.get('q', None)
        
    #     if query is not None:
    #         course_results = Course.objects.search(query)
    #         module_results = Module.objects.search(query)
    #         teacher_results = User.objects.search(query)
            
    #         queryset_chain = chain(
    #             course_results,
    #             module_results
    #         )        
    #         qs = sorted(
    #             queryset_chain, 
    #             key=lambda instance: instance.pk, 
    #             reverse=True)
    #         self.count = len(qs)
    #         return qs
    #     return Course.objects.none()

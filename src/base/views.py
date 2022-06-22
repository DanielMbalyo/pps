from itertools import chain
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render, reverse, get_object_or_404

from src.shop.models import Shop
from src.product.models import UserProduct

class LandingView(TemplateView):
    template_name = 'base/landing.html'

class HomeView(View):
    template_name = 'base/home.html'

    def get(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            product = UserProduct.objects.search(query)
            context = {
                'query': self.request.GET.get('q'),
                'map_api_key': settings.MAP_API_KEY,
                'products': UserProduct.objects.search(query),
            }
            return render(self.request, 'base/home.html', context)
        context = {
            'query': self.request.GET.get('q'),
            'map_api_key': settings.MAP_API_KEY,
            'shops': Shop.objects.all(),
        }
        return render(self.request, 'base/home.html', context)

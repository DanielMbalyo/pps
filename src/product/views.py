import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)

from .forms import ProductForm, UserProductForm
from .models import Product, UserProduct


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/product_list.html"
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
            results = Product.objects.search(query)
            queryset_chain = chain(results)     
            qs = sorted(queryset_chain, key=lambda instance: instance.pk,
                reverse=True)
            self.count = len(qs)
            return qs
        return Product.objects.all()

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = 'instance'
    slug = None

    def get_success_url(self):
        self.object = self.get_object()
        return reverse("product:detail", kwargs={"slug": self.object.slug})

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Product.objects.get_by_slug(slug)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'product/product_form.html'

    def get_success_url(self):
        return reverse('product:list')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        messages.success(self.request, "Successfully Created")
        product.save()
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'

    def get_success_url(self):
        return reverse('product:list')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        messages.success(self.request, "Successfully Updated")
        product.save()
        return super(ProductUpdateView, self).form_valid(form)
        

class ProductRemoveView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('product:list')

    def delete(self, request):
        messages.success(self.request, "Post deleted")
        return super(ProductRemoveView, self).delete(request)

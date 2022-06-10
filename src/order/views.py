import pdfkit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Order,ProductPurchase

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'object'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            if self.request.user.staff:
                results = Order.objects.search(query)
            elif self.request.user.business:
                results = Order.objects.filter(vendor=self.request.user.get_acc()).search(query)
            else:
                results = Order.objects.filter(client=self.request.user.get_acc()).search(query)
            queryset_chain = chain(results)        
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        if self.request.user.staff:
            return Order.objects.all()
        elif self.request.user.business:
            return  Order.objects.filter(vendor=self.request.user.get_acc()).search(query)
        else:
            return Order.objects.filter(client=self.request.user.get_acc()).search(query)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'object'

    def get_object(self):
        return get_object_or_404(Order, order_id=self.kwargs.get('order_id'))

    def get(self, *args, **kwargs):
        context = {
            'object': self.get_object(),
            'items': ProductPurchase.objects.filter(order=self.get_object()),
            'token': self.get_object().order_id.__str__()
        }
        filename = '{}.pdf'.format(self.get_object().order_id)
        template = get_template('order/order_detail.html')
        html = template.render(context)
        options = {
            'encoding': 'UTF-8',
            'javascript-delay':'10', #Optional
            'enable-local-file-access': None, #To be able to access CSS
            'page-size': 'A4',
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
        }
        # config = pdfkit.configuration(wkhtmltopdf='/app/bin/wkhtmltopdf')
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        file_invoice = pdfkit.from_string(html, False, configuration=config, options=options)
        response = HttpResponse(file_invoice, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename = {}'.format(filename)
        return response

class VerifyOwnership(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404
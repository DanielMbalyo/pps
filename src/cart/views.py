from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin

from src.account.forms import LoginForm

from src.billing.models import BillingProfile
from src.order.models import Order, ProductPurchase
from src.product.models import Product, UserProduct
from .models import Cart, CartItem
from decimal import Decimal

class CartUpdateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id'))
        if cart:
            item_id = self.kwargs.get('slug')
            if item_id:
                product = UserProduct.objects.filter(slug=item_id).first()
                item = CartItem.objects.create(cart=cart.first(), product=product)
                subtotal = Decimal(item.cart.subtotal) + Decimal(item.product_total)
                tax_total = subtotal * Decimal(item.cart.tax_percentage) #8.5%
                total = subtotal + Decimal(tax_total)
                item.cart.subtotal = "%.2f" %(subtotal)
                item.cart.tax_total = "%.2f" %(tax_total)
                item.cart.total = "%.2f" %(total)
                item.cart.save()
                messages.success(self.request, "Successful Added To Cart")
                return redirect(item.cart.vendor.get_front_url())
            else:
                messages.success(self.request, "Failed To Add To Cart")
                return redirect(item.cart.vendor.get_front_url())
        return redirect(item.cart.vendor.get_front_url())

class CartRemoveView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id'))
        if cart:
            item_id = self.kwargs.get('slug')
            if item_id:
                product = UserProduct.objects.filter(slug=item_id).first()
                item = CartItem.objects.filter(cart=cart.first(), product=product).distinct().first()
                subtotal = Decimal(item.cart.subtotal) - Decimal(item.product_total)
                tax_total = subtotal * Decimal(item.cart.tax_percentage) #8.5%
                total = subtotal + Decimal(tax_total)
                item.cart.subtotal = "%.2f" %(subtotal)
                item.cart.tax_total = "%.2f" %(tax_total)
                item.cart.total = "%.2f" %(total)
                item.cart.save()
                item.delete()
                messages.success(self.request, "Successful Removed From Cart")
                return redirect(item.cart.vendor.get_front_url())
        return redirect(item.cart.vendor.get_front_url())

class CartClearView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id')).first()
        if cart:
            cart_item = CartItem.objects.filter(cart=cart)
            if cart_item:
                for obj in cart_item:
                    obj.delete()
                messages.success(self.request, "Successful Cleared Cart")
            else:
                messages.success(self.request, "Failed To Clear Cart")
            cart.clear()
        return redirect(cart.vendor.get_front_url())

class CheckoutView(LoginRequiredMixin, TemplateView):
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id')).first()
        if cart:
            cart_item = CartItem.objects.filter(cart=cart)
            if cart_item.count() == 0:
                messages.success(self.request, "Please Add Items To Cart")
                return redirect(cart.vendor.get_front_url())
            order = Order.objects.create(vendor=cart.vendor, total=cart.total)
            cart.clear()
            for obj in cart_item:
                ProductPurchase.objects.create(
                    order=order, product=obj.product, quantity=obj.quantity, amount=obj.product_total
                )
                obj.delete()
            messages.success(self.request, "Order Created Successfully")
            return redirect(order.get_absolute_url())


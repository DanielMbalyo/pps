from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin

from src.account.forms import LoginForm

from src.address.forms import AddressForm
from src.address.models import Address

from src.billing.models import BillingProfile
from src.order.models import Order
from src.product.models import Product, UserProduct
from .models import Cart, CartItem

class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/cart_list.html'

    def get_context_data(self, **kwargs):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        cart_item = CartItem.objects.filter(cart=cart_obj)
        context = super(CartView, self).get_context_data(**kwargs)
        context.update({
            'cart_obj': cart_obj,
            'products' : cart_item,
        })
        return context

class CartUpdateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        if cart_obj:
            item_id = self.kwargs.get('slug')
            if item_id:
                item = UserProduct.objects.filter(slug=item_id).first()
                qty = self.request.GET.get("qty", 1)
                cart_item = CartItem.objects.create(
                    cart=cart_obj, product=item
                )
                messages.success(self.request, "Successful Added To Cart")
                item_added = True
                cart_item.quantity = qty
                cart_item.save()
                return redirect(item.shop.get_front_url())
            else:
                messages.success(self.request, "Failed To Add To Cart")
                return redirect(item.shop.get_front_url())
        return redirect("cart:list")

class CartDeleteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        if cart_obj:
            item_id = self.request.GET.get("product_id")
            if item_id:
                item_instance = get_object_or_404(Product, id=item_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, item=item_instance)
                cart_item.delete()
                flash_message = "Quantity has been updated successfully."
        return redirect("cart:list")

class CartClearView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        if cart_obj:
            count = cart_obj.products.count()
            if count >= 1:
                cart_item = CartItem.objects.filter(cart=cart_obj)
                cart_item.delete()
        return redirect("cart:list")

class CheckoutView(LoginRequiredMixin, TemplateView):
    address_qs = None
    has_card = False
    order_obj = None
    billing_profile = None

    def get(self, request):
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj = None
        if cart_created or cart_obj.products.count() == 0:
            return redirect("cart:list")

        login_form = LoginForm(request=request)
        guest_form = GuestForm(request=request)
        address_form = AddressForm()
        billing_address_id = request.session.get("billing_address_id", None)
        shipping_address_required = not cart_obj.is_digital
        shipping_address_id = request.session.get("shipping_address_id", None)

        self.billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if self.billing_profile is not None:
            if request.user.is_authenticated:
                self.address_qs = Address.objects.filter(billing_profile=self.billing_profile)
            content_type = ContentType.objects.get(app_label='cart', model='cart')
            self.order_obj, order_obj_created = Order.objects.new_or_get(
                self.billing_profile, cart_obj, content_type, cart_obj.id)
            if shipping_address_id:
                self.order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
                del request.session["shipping_address_id"]
            if billing_address_id:
                self.order_obj.billing_address = Address.objects.get(id=billing_address_id) 
                del request.session["billing_address_id"]
            if billing_address_id or shipping_address_id:
                self.order_obj.save()
            has_card = self.billing_profile.has_card

        context = {
            "object": self.order_obj,
            "billing_profile": self.billing_profile,
            "login_form": login_form,
            "guest_form": guest_form,
            "address_form": address_form,
            "address_qs": self.address_qs,
            "has_card": has_card,
            "publish_key": STRIPE_PUB_KEY,
            "shipping_address_required": shipping_address_required,
        }
        return render(self.request, "cart/cart_checkout.html", context)

    def post(self, request):
        is_prepared = self.order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = self.billing_profile.charge(self.order_obj)
            if did_charge:
                self.order_obj.mark_paid() # sort a signal for us
                self.request.session['cart_items'] = 0
                del self.request.session['cart_id']
                if not self.billing_profile.user:
                    self.billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")

class CheckoutDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/checkout_done.html'

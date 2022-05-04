from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (
    AllowAny,
    # IsAuthenticated,
    # IsAdminUser,
    # IsAuthenticatedOrReadOnly,
    )
from rest_framework.response import Response
from rest_framework.views import APIView

from src.order.models import Order
from src.product.models import Product
from src.address.models import Address

from .mixins import TokenMixin
from src.billing.models import BillingProfile
from src.cart.models import Cart, CartItem
from src.address.api.serializers import UserAddressSerializer
from .serializers import CartItemSerializer, CheckoutSerializer, FinalizedCheckoutSerializer

User = settings.AUTH_USER_MODEL
"""
{
	"order_token": "eydvcmRlcl9pZCc6IDU1LCAndXNlcl9jaGVja291dF9pZCc6IDExfQ==",
	"payment_method_nonce": "2bd23ca6-ae17-4bed-85f6-4d00aabcc3b0"
}
Run Python server:
python -m SimpleHTTPServer 8080

"""
class CartAPIView(TokenMixin, APIView):
    authentication_classes = [SessionAuthentication]
	# permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        cart_item = CartItem.objects.filter(cart=cart_obj)
        items = CartItemSerializer(cart_item, many=True)
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        data = {
            "billing_id" : billing_profile.customer_id,
            "cart_id" : cart_obj.id,
            "total": cart_obj.total,
            "subtotal": cart_obj.subtotal,
            "tax_total": cart_obj.tax_total,
            "count": cart_item.count(),
            "items": items.data,
        }
        request.session['cart_token'] = str(self.create_token(data))
        return Response(data)

class CartUpdateAPIView(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, **kwargs):
        product_id = kwargs.get('product_id')
        qty = kwargs.get('qty')
        data = {}
        flash_message = ''
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        print(cart_obj)
        if cart_obj:
            if product_id:
                item_instance = get_object_or_404(Product, id=product_id)
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart_obj, product=item_instance, quantity=qty
                )
                if created:
                    flash_message = "Successfully added to the cart"
                    item_added = True
                # cart_item.quantity = int(qty)
                cart_item.save()
                data = {
                    'message' : flash_message,
                }
        return Response(data)

class CartDeleteAPIView(APIView):
    def get(self, **kwargs):
        product_id = kwargs.get('product_id')
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        if cart_obj:
            item_id = self.request.GET.get("product_id")
            if item_id:
                item_instance = get_object_or_404(Product, id=item_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, item=item_instance)
                cart_item.delete()
                flash_message = "Quantity has been updated successfully."
        # return Response(data)

class CartClearAPIView(APIView):
    def get(self, *args, **kwargs):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        if cart_obj:
            count = cart_obj.products.count()
            if count >= 1:
                cart_item = CartItem.objects.filter(cart=cart_obj)
                cart_item.delete()
        # return Response(data)

class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id is None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404

class CheckoutAPIView(TokenMixin, APIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CheckoutSerializer

    def get(self, request):
        token = request.session.get('cart_token', None)
        if token:
            token_data = self.parse_token(token)
            if token_data['cart_id'] or token_data['count'] == 0:
                data = {
                    "message": "Cart is empty, Fill up some items and try again.",
                    "success": False
                }
        else:
            data = {
                "message": "Cart not found, Fill up some items and try again.",
                "success": False
            }
        data = {
            'billing_id' : token_data['billing_id'],
            "total": token_data['total'],
            "subtotal": token_data['subtotal'],
            "tax_total": token_data['tax_total'],
            "count": token_data['count'],
            "items": token_data['items'],
            "publish_key": settings.STRIPE_PUB_KEY,
        }
        return Response(data)

    def post(self, request, format=None):
        token = request.session.get('cart_token', None)
        token_data = self.parse_token(token)
        data = request.data
        serializer = CheckoutSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            address_id = data.get("address_id")
            billing_id = data.get('billing_id')
            billing_profile = BillingProfile.objects.get(customer_id=billing_id)
            address_qs = Address.objects.filter(billing_profile=billing_profile).first()
            address = UserAddressSerializer(address_qs, many=True)
            content_type = ContentType.objects.get(app_label='cart', model='cart')

            # shipping_address_required = not cart_obj.is_digital
            # has_card = billing_profile.has_card
            cart_obj = Cart.objects.get(id=token_data['cart_id'])
            cart_item = CartItem.objects.filter(cart=cart_obj)
            pack_obj = cart_item.first().get_pack()
            order_obj, order_obj_created = Order.objects.new_or_get(
                billing_profile, pack_obj, content_type, cart_obj.id)
            if not order_obj:
                order_obj.shipping_address = address_qs
                order_obj.billing_address = address_qs
                order_obj.save()
        else:
            data = {
                "message": "what the fuck man"
            }
        data = {
            "object": order_obj.order_id,
            "address_qs": address.data,
        }
        request.session['order_token'] = str(self.create_token(data))
        return Response(data)

class CheckoutFinalizeAPIView(TokenMixin, APIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = FinalizedCheckoutSerializer

    def get(self, request, format=None):
        response = {}
        cart_token = request.session.get('cart_token', None)
        order_token = request.session.get('order_token', None)
        if order_token and cart_token:
            cart_token = self.parse_token(cart_token)
            order_token = self.parse_token(order_token)
            data = {
                "object": order_token['object'],
                'billing_id' : cart_token['billing_id'],
                "total": cart_token['total'],
                "subtotal": cart_token['subtotal'],
                "tax_total": cart_token['tax_total'],
                "count": cart_token['count'],
                "items": cart_token['items'],
                "address_qs": order_token['address_qs'],
            }
            return Response(data)
        else:
            response["message"] = "This method is not allowed"
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        data = request.data
        response = {}
        order_token = request.session.get('order_token', None)
        cart_token = request.session.get('cart_token', None)
        if order_token and cart_token:
            order_id = self.parse_token(order_token).get("order_id")
            cart_id = self.parse_token(order_token).get("cart_id")
            order_obj = Order.objects.get(id=order_id)
            cart_obj = Cart.objects.get(id=cart_id)  
            is_prepared = order_obj.check_done()
            billing_profile = order_obj.billing_profile
            if is_prepared:
                did_charge, crg_msg = billing_profile.charge(order_obj)
                if did_charge:
                    order_obj.mark_paid() # sort a signal for us
                    cart_obj.active = False
                    del self.request.session['cart_id']
                    if not billing_profile.user:
                        billing_profile.set_cards_inactive()
                    response["message"] = "Ordered has been completed."
                    response["success"] = True
                    return Response(response)
                else:
                    print(crg_msg)
                    response["message"] = "Ordered has already been completed."
                    response["success"] = False
                    return Response(response)
                return Response(response)
        else:
            response["message"] = "This method is not allowed"
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
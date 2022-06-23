from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import ( AllowAny, )
from rest_framework.response import Response
from rest_framework.views import APIView

from src.order.models import Order, ProductPurchase
from src.product.models import UserProduct

from src.cart.models import Cart, CartItem
from src.shop.models import Vendor
from .serializers import CartItemSerializer
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class CartAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
	# permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        vendor = Vendor.objects.filter(id=self.kwargs.get('id')).first()
        cart_obj = Cart.objects.filter(vendor=vendor).first()
        cart_item = CartItem.objects.filter(cart=cart_obj)
        items = CartItemSerializer(cart_item, many=True)
        data = {
            "cart_id" : cart_obj.id,
            "total": cart_obj.total,
            "subtotal": cart_obj.subtotal,
            "tax_total": cart_obj.tax_total,
            "count": cart_item.count(),
            "items": items.data,
        }
        return Response(data)

class CartUpdateAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id'))
        if cart:
            item_id = self.kwargs.get('product_id')
            if item_id:
                product = UserProduct.objects.filter(id=item_id).first()
                item = CartItem.objects.create(cart=cart.first(), product=product)
                subtotal = item.cart.subtotal + Decimal(item.product_total)
                tax_total = round(subtotal * Decimal(item.cart.tax_percentage), 2) #8.5%
                total = round(subtotal + Decimal(tax_total), 2)
                item.cart.subtotal = "%.2f" %(subtotal)
                item.cart.tax_total = "%.2f" %(tax_total)
                item.cart.total = "%.2f" %(total)
                item.cart.save()
                data = { 'message' : "Successfully added to the cart", }
            else:
                data = { 'message' : "Failed To Add To Cart", }
        return Response(data)

class CartDeleteAPIView(APIView):    
    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id'))
        if cart:
            item_id = self.kwargs.get('product_id')
            if item_id:
                product = UserProduct.objects.filter(id=item_id).first()
                item = CartItem.objects.filter(cart=cart.first(), product=product).first()
                subtotal = item.cart.subtotal - Decimal(item.product_total)
                tax_total = round(subtotal * Decimal(item.cart.tax_percentage), 2) #8.5%
                total = round(subtotal + Decimal(tax_total), 2)
                item.cart.subtotal = "%.2f" %(subtotal)
                item.cart.tax_total = "%.2f" %(tax_total)
                item.cart.total = "%.2f" %(total)
                item.cart.save()
                item.delete()
                data = { 'message' : "Successfully Removed From Cart", }
            else:
                data = { 'message' : "Failed To Remove From Cart", }
        return Response(data)

class CartClearAPIView(APIView):
    def get(self, *args, **kwargs):
        vendor = Vendor.objects.filter(id=self.kwargs.get('id')).first()
        cart_obj = Cart.objects.filter(vendor=vendor).first()
        if cart_obj:
            cart_item = CartItem.objects.filter(cart=cart_obj)
            if cart_item:
                for obj in cart_item:
                    obj.delete()
                data = { 'message' : "Successful Cleared Cart", }
            else:
                data = { 'message' : "Failed To Clear Cart", }
            cart_obj.clear()
        return Response(data)

class CheckoutAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        cart = Cart.objects.filter(id=self.kwargs.get('id')).first()
        if cart:
            cart_item = CartItem.objects.filter(cart=cart)
            if cart_item.count() == 0:
                data = { "message": "Please Add Items To Cart" }
                return Response(data)
            order = Order.objects.create(vendor=cart.vendor, total=cart.total)
            cart.clear()
            for obj in cart_item:
                ProductPurchase.objects.create(
                    order=order, product=obj.product, quantity=obj.quantity, amount=obj.product_total
                )
                obj.delete()
            data = { 
                "order": order.order_id.__str__(), 
                "message": "Order Created Successfully" 
            }
            return Response(data)

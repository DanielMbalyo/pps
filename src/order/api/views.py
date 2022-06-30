from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect

from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from src.billing.models import BillingProfile, Charge
from src.order.models import Order, ProductPurchase
from src.client.models import Client 
from src.shop.models import Vendor 
from .permissions import IsOwnerAndAuth
from .serializers import OrderSerializer, PurchaseSerializer

import uuid

User = get_user_model()

class OrderCompleteAPIView(APIView):

    def get(self, request, format=None, **kwargs):
        client = Client.objects.filter(id=self.kwargs.get('client')).first()
        order = Order.objects.filter(order_id=self.kwargs.get('id'), client=client).first()
        bill = BillingProfile.objects.filter(client=client).first()
        bill1 = BillingProfile.objects.filter(vendor=order.vendor).first()
        print(order, bill, bill1, client)
        if order and bill and bill1:
            if bill.amount > order.total:
                bill.amount = bill.amount - order.total
                Charge.objects.create(billing=bill, amount=order.total, paid=True, order=order)
                bill.save()
                bill1.amount = bill1.amount + order.total
                Charge.objects.create(billing=bill1, amount=order.total, paid=True, order=order)
                bill1.save()
                order.complete = True
                order.active = False
                order.save()
                data = {
                    'success': True,
                    "message" : "Order Payment Successfully"
                }
            else:
                data = {
                    'success': False,
                    "message" : "No Enough Funds To Complete Payment"
                }
        else:        
            data = {
                'success': False,
                "message" : "Failed To Process Payment"
            }
        return Response(data)

class OrderReceiveAPIView(APIView):

    def get(self, request, format=None, **kwargs):
        order = Order.objects.filter(order_id=self.kwargs.get('id')).first()
        client = Client.objects.filter(id=self.kwargs.get('client')).first()
        order.client = client
        order.save()
        data = {
            "message" : "Order Received Successfully",
            "data" : OrderSerializer(order).data
        }
        return Response(data)

class OrderRetrieveAPIView(APIView):

    def get(self, request, format=None, **kwargs):
        order = Order.objects.filter(order_id=self.kwargs.get('id')).first()
        products = ProductPurchase.objects.filter(order=order)
        items = PurchaseSerializer(products, many=True)
        data = {
            "order_id" : order.order_id,
			"complete" : order.complete, 
            "active" : order.active,  
            "total" : order.total,
            "items": items.data,
        }
        return Response(data)

class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Order.objects.all()
        vendor = self.request.GET.get("vendor")
        client = self.request.GET.get("client")
        if vendor:
            vendor = Vendor.objects.filter(id=vendor).first()
            queryset_list = queryset_list.filter(vendor=vendor).distinct()
        elif client:
            client = Client.objects.filter(id=client).first()
            queryset_list = queryset_list.filter(client=client).distinct()
        return queryset_list

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

from src.billing.models import BillingProfile
from src.order.models import Order 
from src.client.models import Client 
from src.shop.models import Vendor 
from .permissions import IsOwnerAndAuth
from .serializers import OrderSerializer, OrderDetailSerializer

User = get_user_model()

class OrderRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerAndAuth]
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(self.request)
        return Order.objects.filter(billing_profile=billing_profile)

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

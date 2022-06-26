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
from .serializers import BillingSerializer, ChargeSerializer

import uuid

User = get_user_model()

class BillingAPIView(APIView):

    def get(self, request, format=None, **kwargs):
        vendor = self.request.GET.get("vendor")
        client = self.request.GET.get("client")
        billing = BillingProfile.objects.all()
        account = BillingSerializer(billing, many=True)
        if vendor:
            vendor = Vendor.objects.filter(id=vendor).first()
            billing = BillingProfile.objects.filter(vendor=vendor).first()
            account = BillingSerializer(billing)
        elif client:
            client = Client.objects.filter(id=client).first()
            billing = BillingProfile.objects.filter(client=client).first()
            account = BillingSerializer(billing)
        data = {
            "results" : account.data,
        }
        return Response(data)

class ChargeAPIView(APIView):
    serializer_class = ChargeSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]

    def get(self, request, format=None, **kwargs):
        vendor = self.request.GET.get("vendor")
        client = self.request.GET.get("client")
        charges = Charge.objects.all()
        if vendor:
            vendor = Vendor.objects.filter(id=vendor).first()
            billing = BillingProfile.objects.filter(vendor=vendor).first()
            charges = Charge.objects.filter(billing=billing)
        elif client:
            client = Client.objects.filter(id=client).first()
            billing = BillingProfile.objects.filter(client=client).first()
            charges = Charge.objects.filter(billing=billing)
        account = ChargeSerializer(charges, many=True)
        data = {
            "results" : account.data,
        }
        return Response(data)

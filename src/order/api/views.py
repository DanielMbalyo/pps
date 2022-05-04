from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from src.billing.models import BillingProfile
from src.order.models import Order 
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
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(self.request)
        if self.request.user.is_authenticated:
            return Order.objects.filter(billing_profile=billing_profile)
        else:
            return []

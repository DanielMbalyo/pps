from django.contrib import messages
from rest_framework import generics

from src.address.models import Address
from src.billing.models import BillingProfile
from .serializers import AddressSerializer

class AddressCreateAPIView(generics.CreateAPIView):
    model = Address
    serializer_class = AddressSerializer

class AddressListAPIView(generics.ListAPIView):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self, *args, **kwargs):
        billing, _ = BillingProfile.objects.new_or_get(self.request)
        if self.request.user.is_authenticated:
            return Address.objects.filter(billing=billing)
        else:
            return []

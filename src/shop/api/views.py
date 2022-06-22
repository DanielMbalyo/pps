from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics

from .pagination import ShopLimitOffsetPagination, ShopPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAdminUser, IsAuthenticatedOrReadOnly,
    )

from src.shop.models import Shop, Vendor
from .serializers import ShopSerializer, VendorSerializer, ShopCreateSerializer, VendorCreateSerializer

class ShopCreateAPIView(generics.CreateAPIView):
    serializer_class = ShopCreateSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class VendorCreateAPIView(generics.CreateAPIView):
    serializer_class = VendorCreateSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ShopDetailAPIView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    #lookup_url_kwarg = "abc"

class ShopUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        #email send_email

class ShopDeleteAPIView(generics.DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"

class ShopListAPIView(generics.ListAPIView):
    serializer_class = ShopSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    pagination_class = ShopPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Shop.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query)
            ).distinct()
        return queryset_list

class VendorListAPIView(generics.ListAPIView):
    serializer_class = VendorSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    pagination_class = ShopPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Vendor.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query)
            ).distinct()
        return queryset_list
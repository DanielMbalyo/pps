from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics

from .pagination import ProductLimitOffsetPagination, ProductPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAdminUser, IsAuthenticatedOrReadOnly,
)

from src.product.models import Product, UserProduct
from src.shop.models import Vendor

from .serializers import (
    ProductCreateSerializer,
    ProductListSerializer, UserProductListSerializer
)

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    # serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    #lookup_url_kwarg = "abc"

class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        #email send_email

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    pagination_class = ProductPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Product.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
            ).distinct()
        return queryset_list

class UserProductListAPIView(generics.ListAPIView):
    serializer_class = UserProductListSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    pagination_class = ProductPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = UserProduct.objects.all()
        query = self.request.GET.get("id")
        if query:
            vendor = Vendor.objects.filter(id=query).first()
            queryset_list = queryset_list.filter(vendor=vendor).distinct()
        return queryset_list
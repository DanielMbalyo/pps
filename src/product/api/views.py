from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics

from .pagination import ProductLimitOffsetPagination, ProductPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAdminUser, IsAuthenticatedOrReadOnly,
    )

from src.product.models import Product

from .serializers import (
    ProductCreateUpdateSerializer, ProductDetailSerializer,
    ProductListSerializer
    )

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    #lookup_url_kwarg = "abc"

class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        #email send_email

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    # permission_classes = [AllowAny]
    search_fields = ['title', 'body', 'user__username']
    pagination_class = ProductPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Product.objects.filter(package=self.request.package) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)
                    # Q(body__icontains=query)|
                    # Q(user__first_name__icontains=query) |
                    # Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list

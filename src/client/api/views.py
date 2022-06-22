from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics

# from .pagination import ProductLimitOffsetPagination, ProductPageNumberPagination
# from .permissions import IsOwnerOrReadOnly

from rest_framework.permissions import AllowAny

from src.client.models import Client
from .serializers import ClientSerializer, ClientCreateSerializer, ClientFinanceSerializer

class ClientCreateAPIView(generics.CreateAPIView):
    serializer_class = ClientCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class ClientFinanceAPIView(generics.CreateAPIView):
    serializer_class = ClientFinanceSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class ClientDetailAPIView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'slug'
    # permission_classes = [AllowAny]

class ClientUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'slug'
    # permission_classes = [IsOwnerOrReadOnly]
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class ClientListAPIView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['name', 'phone', 'slug', 'account__email']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Client.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query) |
                Q(slug__icontains=query) |
                Q(account__email__icontains=query) 
            ).distinct()
        return queryset_list

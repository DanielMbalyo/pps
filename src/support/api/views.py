from django.db.models import Q

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from .serializers import (
    ContactCreateSerializer,
    NewsletterCreateSerializer,
    )

class ContactAPIView(CreateAPIView):
    serializer_class = ContactCreateSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(package=self.request.package)

class NewsletterAPIView(CreateAPIView):
    serializer_class = NewsletterCreateSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(package=self.request.package, subscribed=True)

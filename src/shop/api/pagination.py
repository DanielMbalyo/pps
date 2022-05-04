from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class ShopLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10

class ShopPageNumberPagination(PageNumberPagination):
    page_size = 20
    
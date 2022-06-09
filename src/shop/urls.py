from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('create/', views.ShopCreateView.as_view(), name="create"),
    path('vendor/', views.VendorCreateView.as_view(), name="vendor"),
    path('summary/', views.ShopSummaryView.as_view(), name="summary"),
    path('complete/', views.ShopCompleteView.as_view(), name="complete"),
    path('policy/', views.ShopPolicyView.as_view(), name="policy"),
    path('', views.ShopListView.as_view(), name="list"),
    path('<slug>/', views.ShopView.as_view(), name="detail"),
    path('<slug>/cat/', views.ShopFrontView.as_view(), name="front"),
    path('<slug>/update', views.ShopUpdateView.as_view(), name="update"),
]
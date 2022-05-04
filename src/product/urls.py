from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('create/', views.ProductCreateView.as_view(), name="create"),
    path('', views.ProductListView.as_view(), name='list'),
    path('<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('<slug>/update', views.ProductUpdateView.as_view(), name="update"),
    path('<slug>/delete', views.ProductRemoveView.as_view(), name="delete"),
]
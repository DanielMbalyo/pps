from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path('create/', views.ServiceCreateView.as_view(), name="create"),
    path('', views.ServiceListView.as_view(), name="list"),
    path('<slug>/', views.ServiceView.as_view(), name="detail"),
    path('<slug>/update', views.ServiceUpdateView.as_view(), name="update"),
]
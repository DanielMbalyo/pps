from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('create/', views.ManagerCreateView.as_view(), name="create"),
    path('', views.ManagerListView.as_view(), name="list"),
    path('<slug>/', views.ManagerView.as_view(), name="detail"),
    path('<slug>/update', views.ManagerUpdateView.as_view(), name="update"),
]

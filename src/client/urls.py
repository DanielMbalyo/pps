from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'client'
urlpatterns = [
    # path('autocomplete/',
    #     views.auto_complete,
    #     name='autocomplete',
    # ),
    path('create/', views.ClientCreateView.as_view(), name="create"),
    path('', views.ClientListView.as_view(), name="list"),
    path('<slug>/', views.ClientView.as_view(), name="detail"),
    path('<slug>/update', views.ClientUpdateView.as_view(), name="update"),
]

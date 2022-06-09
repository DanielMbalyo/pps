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
    path('finance/', views.ClientFinanceView.as_view(), name="finance"),
    path('summary/', views.ClientSummaryView.as_view(), name="summary"),
    path('complete/', views.ClientCompleteView.as_view(), name="complete"),
    path('policy/', views.ClientPolicyView.as_view(), name="policy"),
    path('', views.ClientListView.as_view(), name="list"),
    path('<slug>/', views.ClientView.as_view(), name="detail"),
    path('<slug>/update', views.ClientUpdateView.as_view(), name="update"),
]

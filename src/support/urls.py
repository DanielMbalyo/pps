from django.urls import path
from .views import(
    ContactListView,
    ContactView,
    MailPrefView,
    SingleMailView,
)

app_name = 'support'
urlpatterns = [
    path('contact/', ContactListView.as_view(), name="contact_list"),
    path('contact/<pk>/', ContactView.as_view(), name="contact_detail"),

    path('mail/pref/', MailPrefView.as_view(), name="mail_pref"),
    path('mail/single/<pk>/', SingleMailView.as_view(), name="mail_single"),
]

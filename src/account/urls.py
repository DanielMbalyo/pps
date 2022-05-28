from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', views.SettingView.as_view(), name='settings'),
    path('<uuid>/update/', views.UserUpdateView.as_view(), name="update_user"),
    path('permit/<key>/', views.AdminActivateView.as_view(), name='admin_activate'),
    path('activate/<key>/', views.EmailActivateView.as_view(), name='email_activate'),
    path('deactivate/<key>/', views.DeactivateView.as_view(), name='admin_deactivate'),
    path('resend_activation/', views.EmailActivateView.as_view(), name='resend_activation'),
    path('password/change/', views.ChangePassView.as_view(), name='password_change'),
    path('password/reset/', views.ResetPassView.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/<token>/', views.ResetPassConfirmView.as_view(),
         name='password_reset_confirm'),
]

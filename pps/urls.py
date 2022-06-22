from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('src.account.urls')),
    path('', include('src.base.urls')),
    path('billing/', include('src.billing.urls')),
    path('cart/', include('src.cart.urls')),
    path('client/', include('src.client.urls')),
    path('manager/', include('src.manager.urls')),
    path('order/', include('src.order.urls')),
    path('product/', include('src.product.urls')),
    path('shop/', include('src.shop.urls')),
    path('support/', include('src.support.urls')),
]

urlpatterns += [
    path('api/account/', include('src.account.api.urls', namespace='account_api')),
    path('api/cart/', include('src.cart.api.urls', namespace='cart_api')),
    path('api/client/', include('src.client.api.urls', namespace='client_api')),
    path('api/order/', include('src.order.api.urls', namespace='order_api')),
    path('api/product/', include('src.product.api.urls', namespace='product_api')),
    path('api/shop/', include('src.shop.api.urls', namespace='shop_api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

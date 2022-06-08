from django.contrib import admin

from .models import Client, Finance

# class ClientAdmin(admin.ModelAdmin):
#     list_display=('name', 'account',)
#     search_fields = ['name', ]
# admin.site.register(Client, ClientAdmin)
admin.site.register(Client)
admin.site.register(Finance)


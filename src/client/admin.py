from django.contrib import admin

from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display=('name', 'account',)
    search_fields = ['name', ]
admin.site.register(Client, ClientAdmin)

from django.contrib import admin, messages
from .models import NewsLetter, Contact

admin.site.register(NewsLetter)
admin.site.register(Contact)
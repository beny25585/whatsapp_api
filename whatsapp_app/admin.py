from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'api_key')

admin.site.register(Client, ClientAdmin)
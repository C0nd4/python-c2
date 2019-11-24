from django.contrib import admin
from .models import client, command

admin.site.register(client)
admin.site.register(command)

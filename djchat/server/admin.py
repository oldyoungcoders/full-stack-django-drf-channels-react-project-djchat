from django.contrib import admin

from .models import Category, Server, Channel
# Register your models here.

admin.site.register(Category)
admin.site.register(Server)
admin.site.register(Channel)
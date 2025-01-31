from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'phone_number')

admin.site.register(User, UserAdmin)
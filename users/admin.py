from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'phone_number', 'roles')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'roles')}),
    )

admin.site.register(User, UserAdmin)
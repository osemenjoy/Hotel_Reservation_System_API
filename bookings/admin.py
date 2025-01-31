from django.contrib import admin
from .models import Booking
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('id', 'user', 'room', 'status', 'check_in')
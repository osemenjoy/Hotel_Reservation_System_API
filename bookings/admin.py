from django.contrib import admin
from .models import Booking, Transactions
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('id', 'user', 'room', 'status', 'check_in', 'created_at')
    list_filter = ('created_at',)

@admin.register(Transactions)
class TransactionAdmin(ModelAdmin):
    list_display = ('id', 'user', 'amount', 'booking', 'paid_at')
    list_filter = ('paid_at',)
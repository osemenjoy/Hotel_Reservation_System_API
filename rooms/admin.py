from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from .models import Room, Category

@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ("id", "name", "price", "quantity_available")

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "description")    
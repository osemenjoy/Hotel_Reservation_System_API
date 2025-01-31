from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Room, Category
from .serializers import RoomSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]    
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Room, Category
from .serializers import RoomSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]    

# checkin , checkout, category GET
class SearchRoomView(GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:

            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Available rooms list",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status = status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        if category:
            queryset = Room.objects.select_related("category").filter(category=category).filter(quantity_available__gt = 0)
            return queryset
        if check_in or check_out:
            queryset = Room.objects.filter(quantity_available__gt = 0)
            return queryset
        queryset = Room.objects.filter(quantity_available__gt = 0)
        return queryset
    
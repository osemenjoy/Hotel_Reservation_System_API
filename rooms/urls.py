from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename= "rooms")
router.register(r'category', CategoryViewSet, basename="categories")

urlpatterns = [
    
]
urlpatterns += router.urls
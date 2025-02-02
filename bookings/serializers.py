from rest_framework import serializers
from .models import Booking
from rooms.models import Category, Room

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Booking
        fields = ("id", "user","number_of_rooms", "amount", "status","room", "check_in", "check_out")
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        request = self.context.get("request")
        room = validated_data.get("room")
        number_of_rooms = validated_data.get("number_of_rooms")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        if room.quantity_available > 0:
            room.quantity_available -= 1
            room.save()
            validated_data["amount"] = room.price * number_of_rooms
            booking = Booking.objects.create(**validated_data)
            return booking
        else:
            raise serializers.ValidationError("This room is not available")
    
class BookingCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "")
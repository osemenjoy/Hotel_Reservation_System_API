from django.db import models
import uuid
from users.models import User
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CHECKED_IN", "Checked_in"),
        ("CHECKED_OUT", "Checked_out"),
        ("CANCELLED", "Cancelled")
    ]
    id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.room.name} - {self.status}"

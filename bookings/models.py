from django.db import models
import uuid
from users.models import User
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("CHECKED_IN", "Checked_in"),
        ("COMPLETE", "Complete"),
        ("CANCELLED", "Cancelled")
    ]
    id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_rooms = models.PositiveIntegerField(default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.room.name} "
    
class Transactions(models.Model):
    STATUS_CHOICES = [
        ("SUCCESSFUL", "Successful"),
        ("FAILED", "Failed")
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)


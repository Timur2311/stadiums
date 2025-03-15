from django.db import models
from common.models import BaseModel


class Booking(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="bookings"
    )
    stadium = models.ForeignKey(
        "stadion.Stadium", on_delete=models.CASCADE, related_name="bookings"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

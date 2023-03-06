from django.db import models

# Create your models here.


class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField(default=False)


class BookingDetails(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    room_id = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE)
    comment = models.TextField(null=True)











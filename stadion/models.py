from django.contrib.gis.db import models

# from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import District, Region
from common.models import BaseModel


class Stadium(BaseModel):
    class CapacityChoices(models.TextChoices):
        five = "five", _("5x5")
        eight = "eight", _("8x8")
        eleven = "eleven", _("11x11")

    class StadiumZoneTypeChoices(models.TextChoices):
        open_fields = "open_fields", _("Open Fields")
        close_fields = "close_fields", _("Close Fields")
        hall = "hall", _("Hall")

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stadiums",
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=512)
    guide = models.CharField(max_length=4096, null=True, blank=True)
    location = models.PointField(null=True, blank=True)

    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="stadiums"
    )
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="stadiums"
    )
    capacity = models.CharField(
        max_length=128,
        choices=CapacityChoices.choices,
        default=CapacityChoices.five,
    )
    zone_type = models.CharField(
        max_length=128,
        choices=StadiumZoneTypeChoices.choices,
        default=StadiumZoneTypeChoices.open_fields,
    )
    price = models.DecimalField(_("Price"), max_digits=12, decimal_places=2)
    description = models.TextField()
    opens_at = models.DateTimeField(null=True)
    closes_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)


class Contact(models.Model):
    stadium = models.ForeignKey(
        Stadium, on_delete=models.CASCADE, related_name="contacts"
    )
    type = models.CharField(max_length=255)
    info = models.CharField(max_length=255)


class StadiumMedia(BaseModel):
    class TypeChoices(models.TextChoices):
        PHOTO = "photo", _("Photo")
        VIDEO = "video", _("Video")

    stadium = models.ForeignKey(
        Stadium, on_delete=models.CASCADE, related_name="medias"
    )
    media_type = models.CharField(
        max_length=128, choices=TypeChoices.choices, default=TypeChoices.PHOTO
    )
    file = models.FileField(upload_to="stadium_media/")
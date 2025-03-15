import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created Time")
    )
    updated_time = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated Time")
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        if hasattr(self, "name"):
            return self.name
        if hasattr(self, "title"):
            return self.title
        return str(getattr(self, "id") or super(BaseModel, self))


class Region(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=100, verbose_name=_("Nomi"))
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("Latitude"),
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("Longitude"),
        null=True,
        blank=True,
    )
    

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class District(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, verbose_name=_("Region")
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("Latitude"),
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("Longitude"),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
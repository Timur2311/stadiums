import django_filters
from django.utils.translation import gettext_lazy as _
from stadion.models import Stadium


class StadiumFilterSet(django_filters.FilterSet):

    class Meta:
        model = Stadium
        fields = ["region", "district", "capacity", "zone_type", "is_active"]

from django.db import models
from django.utils.translation import gettext_lazy as _


class PoliticalLocalityType(models.TextChoices):
    TOWN = "TOWN", _("Town")
    CITY = "CITY", _("City")
    STATE = "STATE", _("State")
    FEDERAL = "FEDERAL", _("Federal")


class PoliticalLocality(models.Model):
    """
    This represents the region/area a certain political position may preside over / represent
    For example this could be:
    - the city of New York,
    - the town of Wilton,
    - the state of Hawaii
    - the United States
    """

    geo_json_id = models.UUIDField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=1024, null=False, blank=False)
    type = models.CharField(max_length=32, choices=PoliticalLocalityType.choices, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.type} - {self.name}"

from django.db import models
from django.utils.translation import gettext_lazy as _


class PoliticalLocalityType(models.TextChoices):
    TOWN = "TOWN", _("Town")
    CITY = "CITY", _("City")
    STATE = "STATE", _("State")
    FEDERAL = "FEDERAL", _("Federal")


class PoliticalLocality(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=1024, null=False, blank=False)
    type = models.CharField(choices=PoliticalLocalityType.choices, null=False, blank=False)

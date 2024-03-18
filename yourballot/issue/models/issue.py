from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from yourballot.party import PoliticalTendency


class IssueCategory(models.TextChoices):
    SOCIAL = "SOCIAL", _("Social")
    ECONOMIC = "ECONOMIC", _("Economic")


class Issue(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_id = models.UUIDField(null=False, unique=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    description = models.CharField(max_length=1024, null=False, blank=True, default="")
    category = models.CharField(max_length=64, choices=IssueCategory.choices, null=False, blank=False)
    low_score_tendency = models.CharField(max_length=64, choices=PoliticalTendency.choices, null=False, blank=False)
    high_score_tendency = models.CharField(max_length=64, choices=PoliticalTendency.choices, null=False, blank=False)

    def __str__(self) -> str:
        return f"Issue - {self.name}"

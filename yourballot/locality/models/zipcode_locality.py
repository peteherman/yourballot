from django.db import models

from .political_locality import PoliticalLocality


class ZipcodeLocality(models.Model):
    """
    This represents the relationship from a zipcode to a political locality so we can
    easily translate from a voter's zipcode to the political localities to which they
    belong
    """

    zipcode = models.CharField(max_length=5, null=False, blank=False)
    political_locality = models.ForeignKey(PoliticalLocality, on_delete=models.CASCADE, null=False, blank=False)

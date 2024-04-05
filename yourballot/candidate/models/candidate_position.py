from django.db import models

from yourballot.locality.models import PoliticalLocality


class CandidatePosition(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    locality = models.ForeignKey(PoliticalLocality, on_delete=models.PROTECT)
    term_limit = models.PositiveIntegerField(help_text="The number of days for the term, null if no limit")

    def __str__(self) -> str:
        return f"{self.title} - {self.locality}"
